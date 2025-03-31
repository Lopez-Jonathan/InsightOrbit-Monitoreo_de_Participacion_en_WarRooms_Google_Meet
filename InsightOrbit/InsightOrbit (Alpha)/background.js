// Constantes
const MEET_URL = 'https://meet.google.com/*';
const SLACK_WEBHOOK_URL = 'SLACK_WEBHOOK';
const CHECK_INTERVAL_SECONDS = 0.0000167; // Ajustado a 1 segundo

let targetTabId = null;

// Evento que se dispara cuando se instala la extensión
chrome.runtime.onInstalled.addListener(async () => {
    chrome.alarms.create('extractNames', { periodInMinutes: CHECK_INTERVAL_SECONDS});
    chrome.alarms.create('checkMeetTab', { periodInMinutes: CHECK_INTERVAL_SECONDS }); // Cada segundo
    await updateTargetTabId();
});

// Evento que se dispara cuando el alarm es activado
chrome.alarms.onAlarm.addListener(async (alarm) => {
    if (alarm.name === 'extractNames') {
        extractNames();
    }
    if (alarm.name === 'checkMeetTab') {
        checkMeetTab();  // Ejecuta la función cada vez que se dispare la alarma
    }
});


// Función para actualizar el ID de la pestaña objetivo
async function updateTargetTabId() {
    const tabs = await chrome.tabs.query({ url: MEET_URL });
    targetTabId = tabs.length > 0 ? tabs[0].id : null;
}

// Ejecuta las funciones extracParticipantNames y monitorStyleChanges
async function extractNames() {
    if (!targetTabId) {
        await updateTargetTabId();
        if (!targetTabId) return;
    }
    

    try {
        const tab = await getTab(targetTabId);
        if (!tab) return;

        const [names, _] = await Promise.all([
            executeScriptOnTab(tab.id, extractParticipantNames),
            executeScriptOnTab(tab.id, monitorStyleChanges),
        ]);
        
        await storeNames(names);
    } catch (error) {
        console.error('Error extracting names:', error);
    }
}


// Función para obtener una pestaña por ID
async function getTab(tabId) {
    return new Promise((resolve) => {
        chrome.tabs.get(tabId, (tab) => {
            if (chrome.runtime.lastError) {
                console.error(chrome.runtime.lastError);
                resolve(null);
            }
            resolve(tab);
        });
    });
}

// Función para ejecutar un script en una pestaña
async function executeScriptOnTab(tabId, func) {
    const [result] = await chrome.scripting.executeScript({ target: { tabId }, function: func });
    return result?.result || [];
}

let activeMeetTimer = null;

// Función que abre la lista de participantes en Google Meet
function openParticipantsInMeet(tabId) {
    chrome.scripting.executeScript({
        target: { tabId: tabId },
        function: () => {
            const participantsButton = document.querySelector(
                'button[jsname="A5il2e"][aria-label="Personas"]'
            );

            if (participantsButton) {
                // Verificar si el botón ya está presionado
                const isPressed = participantsButton.getAttribute('aria-pressed') === 'true';
                if (!isPressed) {
                    console.log("Abriendo lista de participantes...");
                    participantsButton.click();
                } else {
                    console.warn("La lista de participantes ya está abierta.");
                }
            } else {
                console.error("Botón de participantes no encontrado.");
            }
        },
    });
}

// Función que cierra la lista de participantes
function closeParticipantsInMeet(tabId) {
    chrome.scripting.executeScript({
        target: { tabId: tabId },
        function: () => {
            const participantsButton = document.querySelector(
                'button[jsname="A5il2e"][aria-label="Personas"]'
            );

            if (participantsButton) {
                // Verificar si el botón está presionado
                const isPressed = participantsButton.getAttribute('aria-pressed') === 'true';
                if (isPressed) {
                    console.log("Cerrando lista de participantes...");
                    participantsButton.click();
                } else {
                    console.warn("La lista de participantes ya está cerrada.");
                }
            } else {
                console.error("Botón de participantes no encontrado.");
            }
        },
    });
}

// Detecta cuando la pestaña de Meet está activa
function checkMeetTab() {
    chrome.tabs.query({ url: MEET_URL }, (tabs) => {
        if (tabs.length > 0) {
            const meetTab = tabs[0];

            // Verifica si la pestaña está activa
            if (meetTab.active) {
                console.log("La pestaña de Meet está activa.");
                closeParticipantsInMeet(meetTab.id)
                // Si no hay un temporizador activo, comienza uno
                if (!activeMeetTimer) {
                    activeMeetTimer = setTimeout(() => {
                        openParticipantsInMeet(meetTab.id);
                        closeParticipantsInMeet(meetTab.id);
                        activeMeetTimer = null; // Reinicia el temporizador
                    }, 60000); // 60000 ms = 1 minuto
                }
            } else {
                console.log("La pestaña de Meet no está activa. Cancelando temporizador.");
                clearTimeout(activeMeetTimer);
                activeMeetTimer = null; // Resetea el temporizador si la pestaña no está activa
                openParticipantsInMeet(meetTab.id)
            }
        } else {
            console.warn("No hay pestañas de Meet abiertas.");
            clearTimeout(activeMeetTimer); // Asegúrate de limpiar el temporizador si no hay pestañas de Meet
            activeMeetTimer = null;
        }
    });
}


// Función para almacenar nombres en Local Storage
async function storeNames(names) {
    const { participantNames = [] } = await chrome.storage.local.get('participantNames');
    const allNames = [...new Set([...participantNames, ...names])];
    
    // Solo guardar si hay cambios
    if (participantNames.length !== allNames.length) {
        await chrome.storage.local.set({ participantNames: allNames });
        console.log('Names stored in Local Storage:', allNames);
    }
}

// Función para extraer nombres de participantes
function extractParticipantNames() {
    const nameElements = document.querySelectorAll('[role="listitem"] .zWGUib');
    const collaboratorsDiv = document.querySelector('.V6tdP');
    const moreGuestsDiv = document.querySelector('.Vp3iz');

    if (!collaboratorsDiv) {
        console.log('No se encontró la sección de colaboradores.');
        return [];
    }

    return Array.from(nameElements).filter(el => {
        const isPresenting = el.nextElementSibling && el.nextElementSibling.textContent === 'Presentación';
        const isInCollaboratorsSection = collaboratorsDiv.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING;

        if (moreGuestsDiv) {
            return !isPresenting && isInCollaboratorsSection && (el.compareDocumentPosition(moreGuestsDiv) & Node.DOCUMENT_POSITION_FOLLOWING);
        }
        return !isPresenting && isInCollaboratorsSection;
    }).map(el => el.textContent);
}

// Función para monitorear cambios en estilos
function monitorStyleChanges() {
    const collaboratorsDiv = document.querySelector('.V6tdP');
    const moreGuestsDiv = document.querySelector('.Vp3iz');
    const targetDivs = document.querySelectorAll('[role="listitem"]');
    
    const groupSize = 1;
    const totalParticipants = targetDivs.length;
    const observerCount = Math.max(Math.ceil(totalParticipants / groupSize), 1); // Mínimo 1 observador

    console.log(`${observerCount} observer(s) created for ${totalParticipants} participants.`);
    
    // Función para procesar participantes
    const processParticipant = (presentationElement, nameElement, speaking) => {
        if (presentationElement && presentationElement.textContent === 'Presentación') {
            console.log(`Skipping participant ${nameElement?.textContent || ''} due to screen sharing.`);
            return;
        }

        if (speaking && nameElement) {
            const name = nameElement.textContent;
            console.log('Speaker name detected:', name);
            chrome.runtime.sendMessage({ type: 'currentSpeakerDetected', speaker: name });
        } else if (!speaking && nameElement) {
            const name = nameElement.textContent;
            console.log('Speaker stopped:', name);
            chrome.runtime.sendMessage({ type: 'currentSpeakerStopped', speaker: name });
        }
    };

    // Función para verificar estilos
    const checkStyles = (participants) => {
        participants.forEach(targetDiv => {
            const nameElement = targetDiv.querySelector('.zWGUib');
            const presentationElement = targetDiv.querySelector('.d93U2d.qrLqp');
            const styleElements = targetDiv.querySelectorAll('div[jscontroller="ES310d"] > div');
            const speaking = Array.from(styleElements).some(el => {
                const style = window.getComputedStyle(el);
                return style.backgroundPositionX !== '0px';
            });

            const isInCollaboratorsSection = collaboratorsDiv.compareDocumentPosition(targetDiv) & Node.DOCUMENT_POSITION_FOLLOWING;
            if (moreGuestsDiv) {
                const isBeforeMoreGuests = targetDiv.compareDocumentPosition(moreGuestsDiv) & Node.DOCUMENT_POSITION_PRECEDING;
                if (isInCollaboratorsSection && !isBeforeMoreGuests) {
                    processParticipant(presentationElement, nameElement, speaking);
                }
            } else if (isInCollaboratorsSection) {
                processParticipant(presentationElement, nameElement, speaking);
            }
        });
    };

    // Crear observadores por cada grupo de participantes
    for (let i = 0; i < observerCount; i++) {
    const start = i * groupSize;
    const end = start + groupSize;
    const participantsGroup = Array.from(targetDivs).slice(start, end);

    const observer = new MutationObserver(mutations => {
        for (const mutation of mutations) {
            console.log(`Mutation detected: ${mutation.type}`);  // Indica qué tipo de mutación fue detectada
            if (mutation.type === 'attributes' && mutation.attributeName === 'style') {
                console.log('Detected style change!');
                checkStyles(participantsGroup);
                break;
            }
        }
    });

    participantsGroup.forEach(targetDiv => {
        observer.observe(targetDiv, { childList: true, subtree: true, attributes: true, attributeFilter: ['style'] });
    });
}

    // Ejecutar chequeo inicial para todos los participantes
    checkStyles(Array.from(targetDivs));
}



const timers = {};

// Función para iniciar temporizador
async function startTimer(name) {
    if (!name) {
        console.error('Cannot start timer: name is undefined.');
        return;
    }

    const { timers: storedTimers = {} } = await chrome.storage.local.get('timers');
    const startTime = storedTimers[name] ? Date.now() - (storedTimers[name].elapsed * 1000) : Date.now();
    
    timers[name] = { startTime, intervalId: setInterval(async () => {
        if (timers[name]) {
            const elapsed = Math.floor((Date.now() - timers[name].startTime) / 1000);
            console.log(`Timer running for ${name}: ${elapsed}s`);

            const { timers: updatedTimers = {} } = await chrome.storage.local.get('timers');
            updatedTimers[name] = { elapsed };
            await chrome.storage.local.set({ timers: updatedTimers });
        }
    }, 1000) };
}

// Función para detener temporizador
async function stopTimer(name) {
    if (!name) {
        console.error('Cannot stop timer: name is undefined.');
        return;
    }

    if (timers[name]) {
        clearInterval(timers[name].intervalId);
        console.log(`Stopping timer for ${name}`);
        const elapsed = Math.floor((Date.now() - timers[name].startTime) / 1000);

        const { timers: storedTimers = {} } = await chrome.storage.local.get('timers');
        storedTimers[name] = { elapsed };
        await chrome.storage.local.set({ timers: storedTimers });

        delete timers[name];
    }
}

// Evento que escucha los mensajes
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    switch (message.type) {
        case 'currentSpeakerDetected':
            handleSpeakerDetected(message.speaker);
            break;

        case 'currentSpeakerStopped':
            stopTimer(message.speaker);
            break;

        case 'sendToSlack':
            handleSendToSlack(message.data, sendResponse);
            return true; // Mantener la conexión abierta para el sendResponse asíncrono

        default:
            console.log('Unrecognized message type:', message.type);
    }
});

// Manejo del mensaje 'currentSpeakerDetected'
async function handleSpeakerDetected(speaker) {
    if (!speaker) {
        console.error('Speaker name is undefined.');
        return;
    }

    const { participantNames = [] } = await chrome.storage.local.get('participantNames');
    participantNames.forEach(name => {
        if (name !== speaker) {
            stopTimer(name);
        }
    });

    await startTimer(speaker);
}

// Manejo del mensaje 'sendToSlack'
async function handleSendToSlack(data, sendResponse) {
    try {
        const { timers = {} } = await chrome.storage.local.get('timers');
        const extractedNames = Object.keys(timers).filter(name => timers[name].elapsed > 0);

        const params = new URLSearchParams();
        params.append('payload', JSON.stringify({
            text: `Incident ID(s): ${data.id}\nTitle(s): ${data.titles}\nMetrics: ${data.metrics}\nSites: ${data.sites}\nProducts: ${data.products}\nNames: ${extractedNames.join(', ')}`
        }));

        const response = await fetch(SLACK_WEBHOOK_URL, {
            method: 'POST',
            body: params,
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        });

        if (!response.ok) {
            throw new Error(`Slack API error: ${response.statusText}`);
        }

        console.log('Data sent to Slack successfully:', data);
        sendResponse({ success: true });
    } catch (error) {
        console.error('Error sending to Slack:', error);
        sendResponse({ success: false, error: error.message });
    }
}




















































