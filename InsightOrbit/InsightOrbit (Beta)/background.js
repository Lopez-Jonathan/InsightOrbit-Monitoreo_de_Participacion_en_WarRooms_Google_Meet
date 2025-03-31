// Constantes
const MEET_URL = 'https://meet.google.com/*'; //Variable URL basado en un patron (TODAS LAS MEETS)
const SLACK_WEBHOOK_URL = 'URL_WEBHOOK_SLACK'; //Direccion URL del WebHook donde se envian los datos
const CHECK_INTERVAL_SECONDS = 0.0000167; // Ajustado a 1 segundo

let targetTabId = null; //Inicializa la variable con valor NULL
let activeMeetTimer = null; //Inicializada la variable con valor NULL
const timers = {}; //Inicializamos el diccionario vacio

// Evento que se dispara cuando se instala la extensión
chrome.runtime.onInstalled.addListener(async () => {
    chrome.alarms.create('extractNames', { periodInMinutes: CHECK_INTERVAL_SECONDS}); // Ejecucion casi continua
    chrome.alarms.create('checkMeetTab', { periodInMinutes: CHECK_INTERVAL_SECONDS}); // Ejecucion casi continua
    continuouslyUpdateTargetTabId();
});

// Evento que se dispara cuando el alarm es activado
chrome.alarms.onAlarm.addListener(async (alarm) => {
    if (alarm.name === 'extractNames') {
        extractNames(); // Ejecuta la función cada vez que se dispare la alarma
    }
    if (alarm.name === 'checkMeetTab') {
        checkMeetTab();  // Ejecuta la función cada vez que se dispare la alarma
    }
});


// Función para actualizar continuamente el ID de la pestaña objetivo
async function continuouslyUpdateTargetTabId() {
    const tabs = await chrome.tabs.query({ url: MEET_URL });
    if (tabs.length > 0) {
        targetTabId = tabs[0].id;
        console.log(`Pestaña de Meet encontrada: ${targetTabId}`);
    } else {
        console.log('Reintentando encontrar una pestaña de Meet...');
    }
}

//Se ejecuta al cerrar la pestaña de Google Meet
chrome.tabs.onRemoved.addListener(function (tabId, removeInfo) {
    if (tabId === targetTabId) {
        // Intentar abrir el popup primero
        chrome.action.openPopup();

        // Usar un pequeño retraso para asegurar que el popup esté abierto
        setTimeout(() => {
            handleTabClose().then(() => {
                console.log("Todas las operaciones se completaron correctamente.");
            }).catch(error => {
                console.error("Error durante el manejo de la pestaña cerrada:", error);
            });
        }, 500); // Ajusta el tiempo según sea necesario
    }
});

//Envuelve mediante una promesa general al resto de funciones a ejecutar. Garantiza el orden de ejecucion de las mismas
function handleTabClose() {
    return new Promise((resolve, reject) => {
        // Primero intentar enviar datos a Slack
        sendDataToSlack()
            .catch(error => {
                console.warn("Fallo al enviar datos a Slack:", error);
                // Continuar incluso si hay un error al enviar a Slack
                return null;
            })
            .then(() => {
                // Crear el archivo de texto
                return createDataFile();
            })
            .then(() => {
                // Limpiar Local Storage
                return clearLocalStorage();
            })
            .then(() => {
                resolve();
            })
            .catch(error => {
                reject(error);
            });
    });
}

// Comunicación con la función ubicada en popup.js
function sendDataToSlack() {
    return new Promise((resolve) => {
        // Envía un mensaje a la función en popup.js
        chrome.runtime.sendMessage({ type: 'closeTab', action: 'executeHandleSlackSend' }, response => {
            if (response && response.success) {
                console.log("Datos enviados a Slack correctamente.");
            } else {
                console.warn("Error o datos no enviados a Slack. Continuando...");
            }
            resolve(); // Continuar independientemente del éxito o fallo
        });

        // Manejo de errores en caso de que la conexión con el runtime falle
        if (chrome.runtime.lastError) {
            console.error("Error de runtime:", chrome.runtime.lastError.message);
            resolve(); // Continuar incluso si hay un error
        }
    });
}

// Crea el archivo de Backup
function createDataFile() {
    // Retorna una promesa para manejar la operación de creación de archivo de forma asíncrona
    return new Promise((resolve, reject) => {
        // Obtiene los datos necesarios desde el almacenamiento local de Chrome: 'participantNames', 'timers' y 'slackData'
        chrome.storage.local.get(['participantNames', 'timers', 'slackData'], function (result) {
            // Desestructura los resultados obtenidos del almacenamiento local
            const { participantNames, timers, slackData } = result;
            
            // Inicializa las variables con los datos obtenidos, o usa valores predeterminados si no existen
            const allNames = participantNames || []; // Lista de nombres de participantes
            const timersData = timers || {}; // Datos de temporizadores
            
            // Filtra los nombres que tienen tiempo registrado (es decir, aquellos con un temporizador con tiempo transcurrido > 0)
            const namesWithTime = Object.keys(timersData)
                .filter(name => timersData[name].elapsed > 0);

            // Filtra los nombres que no tienen tiempo registrado (es decir, aquellos sin temporizador o con tiempo 0)
            const namesWithoutTime = allNames.filter(name => !namesWithTime.includes(name));

            // Prepara los datos para escribir en el archivo
            const data = `
                ID: ${slackData.id || 'N/A'}
                Titles: ${slackData.titles || 'N/A'}
                Metrics: ${slackData.metrics || 'N/A'}
                Products: ${slackData.products || 'N/A'}
                Sites: ${slackData.sites || 'N/A'}

                Nombres con tiempo registrado:
                ${namesWithTime.join(', ') || 'Ninguno'}

                Nombres sin tiempo registrado:
                ${namesWithoutTime.join(', ') || 'Ninguno'}
            `;

            // Define el nombre del archivo basado en el ID del incidente (si existe) o un nombre predeterminado
            const fileName = slackData.id ? `${slackData.id}.txt` : 'incident_data.txt';

            // Inicia la descarga del archivo como un archivo de texto con los datos formateados
            chrome.downloads.download({
                url: 'data:text/plain,' + encodeURIComponent(data), // Codifica los datos en formato URL para crear un archivo de texto
                filename: fileName, // Usa el nombre del archivo basado en el ID o un nombre por defecto
                saveAs: true // Indica que debe abrirse la ventana de guardado para que el usuario elija dónde guardar el archivo
            }, function (downloadId) {
                // Si ocurre un error al intentar crear el archivo, se maneja con chrome.runtime.lastError
                if (chrome.runtime.lastError) {
                    console.error("Error al crear el archivo:", chrome.runtime.lastError.message);
                    // Rechaza la promesa con el error ocurrido
                    reject(chrome.runtime.lastError);
                } else {
                    // Si la descarga fue exitosa, se imprime un mensaje de éxito en la consola
                    console.log("Archivo de texto creado correctamente.");
                    // Resuelve la promesa con el ID de descarga del archivo
                    resolve(downloadId);
                }
            });
        });
    });
}

// Limpia completamente el Local Storage
function clearLocalStorage() {
    // Retorna una promesa para manejar el resultado de la operación de limpieza de manera asíncrona
    return new Promise((resolve, reject) => {
        // Llama al método 'clear' de 'chrome.storage.local' para borrar todo el almacenamiento local
        chrome.storage.local.clear(function () {
            // Si ocurrió un error durante la operación 'clear', se maneja con chrome.runtime.lastError
            if (chrome.runtime.lastError) {
                // Si hubo un error, muestra un mensaje de error en la consola con el mensaje de error proporcionado
                console.error("Error al limpiar Local Storage:", chrome.runtime.lastError.message);
                // Rechaza la promesa, pasando el error capturado
                reject(chrome.runtime.lastError);
            } else {
                // Si la operación fue exitosa, muestra un mensaje de éxito en la consola
                console.log("Local Storage completamente limpiado.");
                // Resuelve la promesa para indicar que la operación se completó correctamente
                resolve();
            }
        });
    });
}


// Ejecuta las funciones extractParticipantNames y monitorStyleChanges dentro de la pestaña
async function extractNames() {
    // Verifica si 'targetTabId' está definido, es decir, si se ha encontrado la pestaña de Google Meet
    if (!targetTabId) {
        console.warn('No se ha encontrado la pestaña de Meet todavía. Reintentando...');
        return; // Si no se encuentra la pestaña, muestra una advertencia y termina la ejecución
    }

    try {
        // Obtiene la pestaña mediante su ID utilizando la función 'getTab'
        const tab = await getTab(targetTabId);
        if (!tab) return; // Si no se encuentra la pestaña, termina la ejecución

        // Ejecuta dos funciones asincrónicas en paralelo dentro de la pestaña usando 'executeScriptOnTab':
        // - 'extractParticipantNames' para extraer los nombres de los participantes
        // - 'monitorStyleChanges' para monitorear cambios en el estilo de la página (probablemente cambios en la UI)
        const [names, _] = await Promise.all([
            executeScriptOnTab(tab.id, extractParticipantNames),  // Extrae los nombres de los participantes
            executeScriptOnTab(tab.id, monitorStyleChanges),     // Monitorea los cambios de estilo en la pestaña
        ]);
        
        // Una vez que se han obtenido los nombres, los guarda usando la función 'storeNames'
        await storeNames(names);
    } catch (error) {
        // Si ocurre un error en cualquiera de las operaciones anteriores, captura el error y muestra el mensaje
        console.error('Error extracting names:', error);
    }
}



// Función para obtener una pestaña por ID
async function getTab(tabId) {
    return new Promise((resolve) => {
        chrome.tabs.get(tabId, (tab) => {
            if (chrome.runtime.lastError) {
                console.error(chrome.runtime.lastError);

                const interval = setInterval(async () => {
                    // Si la pestaña no existe, ejecutamos la función para encontrar una nueva pestaña de Meet
                    continuouslyUpdateTargetTabId();
                }, 60000);

                resolve(null); // Retornamos null ya que no se pudo obtener la pestaña
            } else {
                resolve(tab); // Retornamos la pestaña si existe
            }
        });
    });
}


// Función para ejecutar otras funciones en una pestaña
async function executeScriptOnTab(tabId, func) {
    const [result] = await chrome.scripting.executeScript({ target: { tabId }, function: func });
    return result?.result || [];
}

// Función que abre la lista de participantes en Google Meet y maneja el desplazamiento de la barra
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

                // Ahora controlamos el scroll si es necesario
                const participantsList = document.querySelector('[aria-live="polite"]');
                if (participantsList) {
                    // Verificamos si hay una barra de desplazamiento
                    const scrollHeight = participantsList.scrollHeight;
                    const clientHeight = participantsList.clientHeight;
                    const scrollTop = participantsList.scrollTop;

                    // Si la lista tiene suficiente contenido y la barra está desplazada hacia abajo
                    if (scrollHeight > clientHeight) {
                        // Si la barra está arriba, desplazamos hacia abajo
                        if (scrollTop === 0) {
                            console.log("Deslizando hacia abajo...");
                            participantsList.scrollTo(0, scrollHeight); // Desliza al fondo
                        }
                        // Si la barra está abajo, desplazamos hacia arriba
                        else if (scrollTop + clientHeight === scrollHeight) {
                            console.log("Deslizando hacia arriba...");
                            participantsList.scrollTo(0, 0); // Desliza al principio
                        }
                    }
                } else {
                    console.error("No se encontró la lista de participantes.");
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
    // Selecciona todos los elementos que representan los nombres de los participantes
    const nameElements = document.querySelectorAll('[role="listitem"] .zWGUib');
    
    // Selecciona el contenedor de la sección de "Colaboradores" (posiblemente donde se listan los participantes principales)
    const collaboratorsDiv = document.querySelector('.V6tdP');
    
    // Selecciona el contenedor de la sección de "Más invitados" (donde se agrupan participantes secundarios u opcionales)
    const moreGuestsDiv = document.querySelector('.Vp3iz');

    // Si no se encuentra la sección de colaboradores, se registra un mensaje en la consola y se retorna un array vacío
    if (!collaboratorsDiv) {
        console.log('No se encontró la sección de colaboradores.');
        return [];
    }

    // Filtra los elementos seleccionados para obtener solo los nombres válidos
    return Array.from(nameElements).filter(el => {
        // Verifica si el participante está presentando (esto se basa en un texto asociado al elemento siguiente)
        const isPresenting = el.nextElementSibling && el.nextElementSibling.textContent === 'Presentación';
        
        // Verifica si el participante pertenece a la sección de "Colaboradores"
        const isInCollaboratorsSection = collaboratorsDiv.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING;

        // Si existe la sección de "Más invitados", asegura que el participante:
        // 1. No esté presentando
        // 2. Esté en la sección de "Colaboradores"
        // 3. No esté después de la sección de "Más invitados"
        if (moreGuestsDiv) {
            return !isPresenting && isInCollaboratorsSection && (el.compareDocumentPosition(moreGuestsDiv) & Node.DOCUMENT_POSITION_FOLLOWING);
        }

        // Si no existe la sección de "Más invitados", solo verifica que no esté presentando y que esté en la sección de "Colaboradores"
        return !isPresenting && isInCollaboratorsSection;
    }).map(el => el.textContent); // Mapea los elementos filtrados para devolver solo el texto (nombre del participante)
}


// Función para monitorear cambios en estilos
function monitorStyleChanges() {
    // Selecciona la sección de "Colaboradores" y "Más invitados", y todos los elementos de los participantes
    const collaboratorsDiv = document.querySelector('.V6tdP');
    const moreGuestsDiv = document.querySelector('.Vp3iz');
    const targetDivs = document.querySelectorAll('[role="listitem"]');  // Lista de todos los participantes

    // Define el tamaño del grupo de observadores y calcula la cantidad de observadores necesarios
    const groupSize = 1;  // Número de participantes por observador (puede ser ajustado)
    const totalParticipants = targetDivs.length;  // Número total de participantes
    const observerCount = Math.max(Math.ceil(totalParticipants / groupSize), 1); // Calcula el número mínimo de observadores, garantizando al menos uno

    // Imprime en consola la cantidad de observadores que se han creado
    console.log(`${observerCount} observer(s) created for ${totalParticipants} participants.`);

    // Función para procesar cada participante
    const processParticipant = (presentationElement, nameElement, speaking) => {
        // Si el participante está en "Presentación", se omite
        if (presentationElement && presentationElement.textContent === 'Presentación') {
            console.log(`Skipping participant ${nameElement?.textContent || ''} due to screen sharing.`);
            return;  // Si está en presentación, no se realiza ninguna acción
        }

        // Si el participante está hablando, se procesa su nombre
        if (speaking && nameElement) {
            const name = nameElement.textContent;
            console.log('Speaker name detected:', name);
            // Envía un mensaje a la extensión indicando que se detectó al hablante
            chrome.runtime.sendMessage({ type: 'currentSpeakerDetected', speaker: name });
        } else if (!speaking && nameElement) {
            // Si el participante deja de hablar, se procesa su nombre
            const name = nameElement.textContent;
            console.log('Speaker stopped:', name);
            // Envía un mensaje a la extensión indicando que el hablante dejó de hablar
            chrome.runtime.sendMessage({ type: 'currentSpeakerStopped', speaker: name });
        }
    };

    // Función para verificar los estilos de los participantes
    const checkStyles = (participants) => {
        participants.forEach(targetDiv => {
            // Obtiene los elementos que contienen el nombre y el estado de presentación del participante
            const nameElement = targetDiv.querySelector('.zWGUib');
            const presentationElement = targetDiv.querySelector('.d93U2d.qrLqp');
            // Obtiene los elementos de estilo para verificar si el participante está hablando
            const styleElements = targetDiv.querySelectorAll('div[jscontroller="ES310d"] > div');
            // Verifica si alguno de los elementos de estilo tiene un cambio que indica que está hablando
            const speaking = Array.from(styleElements).some(el => {
                const style = window.getComputedStyle(el);
                return style.backgroundPositionX !== '0px';  // Si el fondo de la posición X no es '0px', significa que está hablando
            });

            // Verifica si el participante está en la sección de "Colaboradores"
            const isInCollaboratorsSection = collaboratorsDiv.compareDocumentPosition(targetDiv) & Node.DOCUMENT_POSITION_FOLLOWING;

            // Si hay una sección de "Más invitados", verifica que el participante esté antes de esa sección
            if (moreGuestsDiv) {
                const isBeforeMoreGuests = targetDiv.compareDocumentPosition(moreGuestsDiv) & Node.DOCUMENT_POSITION_PRECEDING;
                if (isInCollaboratorsSection && !isBeforeMoreGuests) {
                    // Si está en la sección de colaboradores y no está en "Más invitados", se procesa el participante
                    processParticipant(presentationElement, nameElement, speaking);
                }
            } else if (isInCollaboratorsSection) {
                // Si no hay "Más invitados", solo se verifica que esté en "Colaboradores"
                processParticipant(presentationElement, nameElement, speaking);
            }
        });
    };

    // Crear un observador para cada grupo de participantes
    for (let i = 0; i < observerCount; i++) {
        const start = i * groupSize;  // Calcula el inicio del grupo de participantes
        const end = start + groupSize;  // Calcula el final del grupo de participantes
        const participantsGroup = Array.from(targetDivs).slice(start, end);  // Extrae el grupo de participantes correspondiente

        // Crea un observador de mutaciones para cada grupo de participantes
        const observer = new MutationObserver(mutations => {
            for (const mutation of mutations) {
                console.log(`Mutation detected: ${mutation.type}`);  // Muestra el tipo de mutación detectada
                // Si se detecta un cambio en los atributos (por ejemplo, cambios en el estilo)
                if (mutation.type === 'attributes' && mutation.attributeName === 'style') {
                    console.log('Detected style change!');
                    // Verifica los estilos de los participantes del grupo
                    checkStyles(participantsGroup);
                    break;  // Detiene el proceso una vez que se detecta el cambio de estilo
                }
            }
        });

        // Observa los cambios en los elementos del grupo de participantes
        participantsGroup.forEach(targetDiv => {
            observer.observe(targetDiv, { childList: true, subtree: true, attributes: true, attributeFilter: ['style'] });
        });
    }

    // Realiza un chequeo inicial de todos los participantes
    checkStyles(Array.from(targetDivs));
}

// Función para iniciar temporizador
async function startTimer(name) {
    // Verifica si el nombre del temporizador está definido
    if (!name) {
        console.error('Cannot start timer: name is undefined.');  // Si no está definido, muestra un error en la consola
        return;  // Finaliza la función
    }

    // Recupera los temporizadores almacenados previamente desde el almacenamiento local
    const { timers: storedTimers = {} } = await chrome.storage.local.get('timers');
    
    // Establece el tiempo de inicio del temporizador, o calcula el tiempo transcurrido si el temporizador ya existe
    const startTime = storedTimers[name] ? Date.now() - (storedTimers[name].elapsed * 1000) : Date.now();
    
    // Inicializa el temporizador para el nombre dado y lo almacena en el objeto global 'timers'
    timers[name] = {
        startTime,  // Guarda el tiempo de inicio del temporizador
        intervalId: setInterval(async () => {
            // Verifica si el temporizador aún está activo para el nombre dado
            if (timers[name]) {
                // Calcula el tiempo transcurrido en segundos desde que comenzó el temporizador
                const elapsed = Math.floor((Date.now() - timers[name].startTime) / 1000);
                console.log(`Timer running for ${name}: ${elapsed}s`);  // Muestra el tiempo transcurrido en la consola

                // Recupera los temporizadores almacenados nuevamente desde el almacenamiento local
                const { timers: updatedTimers = {} } = await chrome.storage.local.get('timers');
                
                // Actualiza el temporizador correspondiente con el nuevo tiempo transcurrido
                updatedTimers[name] = { elapsed };
                
                // Guarda los temporizadores actualizados en el almacenamiento local
                await chrome.storage.local.set({ timers: updatedTimers });
            }
        }, 1000)  // Actualiza el temporizador cada 1 segundo
    };
}

// Función para detener temporizador
async function stopTimer(name) {
    // Verifica si el nombre del temporizador está definido
    if (!name) {
        console.error('Cannot stop timer: name is undefined.');  // Si no está definido, muestra un error en la consola
        return;  // Finaliza la ejecución de la función
    }

    // Verifica si el temporizador existe para el nombre dado
    if (timers[name]) {
        // Detiene el temporizador utilizando el ID del intervalo almacenado
        clearInterval(timers[name].intervalId);
        console.log(`Stopping timer for ${name}`);  // Muestra un mensaje en la consola indicando que se detuvo el temporizador

        // Calcula el tiempo transcurrido en segundos desde el inicio del temporizador
        const elapsed = Math.floor((Date.now() - timers[name].startTime) / 1000);

        // Recupera los temporizadores almacenados previamente desde el almacenamiento local
        const { timers: storedTimers = {} } = await chrome.storage.local.get('timers');
        
        // Actualiza el temporizador correspondiente con el tiempo transcurrido
        storedTimers[name] = { elapsed };
        
        // Guarda los temporizadores actualizados en el almacenamiento local
        await chrome.storage.local.set({ timers: storedTimers });

        // Elimina el temporizador de la variable global 'timers'
        delete timers[name];
    }
}

// Evento que escucha los mensajes
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    // El 'switch' evalúa el tipo de mensaje recibido
    switch (message.type) {
        // Si el mensaje tiene tipo 'currentSpeakerDetected'
        case 'currentSpeakerDetected':
            handleSpeakerDetected(message.speaker);  // Llama a la función que maneja la detección del orador
            break;

        // Si el mensaje tiene tipo 'currentSpeakerStopped'
        case 'currentSpeakerStopped':
            stopTimer(message.speaker);  // Llama a la función que detiene el temporizador del orador
            break;

        // Si el mensaje tiene tipo 'sendToSlack'
        case 'sendToSlack':
            handleSendToSlack(message.data, sendResponse);  // Llama a la función que maneja el envío a Slack
            return true;  // Devuelve 'true' para mantener la conexión abierta y permitir la respuesta asíncrona

        // Caso por defecto: Si el tipo de mensaje no se reconoce
        default:
            console.log('Unrecognized message type:', message.type);  // Muestra un mensaje de advertencia en la consola
    }
});


// Manejo del mensaje 'currentSpeakerDetected'
async function handleSpeakerDetected(speaker) {
    // Verifica si el nombre del orador está definido
    if (!speaker) {
        console.error('Speaker name is undefined.');  // Si no está definido, muestra un error en la consola
        return;  // Sale de la función si el nombre del orador no está definido
    }

    // Recupera los nombres de los participantes almacenados localmente desde el almacenamiento de Chrome
    const { participantNames = [] } = await chrome.storage.local.get('participantNames');

    // Itera sobre los nombres de los participantes
    participantNames.forEach(name => {
        // Si el nombre del participante no es el del orador actual
        if (name !== speaker) {
            stopTimer(name);  // Detiene el temporizador del participante que no es el orador
        }
    });

    // Inicia un temporizador para el orador actual
    await startTimer(speaker);
}


// Manejo del mensaje 'sendToSlack'
async function handleSendToSlack(data, sendResponse) {
    try {
        // Recupera los temporizadores almacenados localmente en el almacenamiento de Chrome
        const { timers = {} } = await chrome.storage.local.get('timers');

        // Filtra los nombres de los participantes que tienen un tiempo de temporizador mayor que 0
        const extractedNames = Object.keys(timers).filter(name => timers[name].elapsed > 0);

        // Asegurar que los datos faltantes se rellenen con "N/A"
        const sanitizedData = {
            id: data.id || "N/A",
            titles: data.titles || "N/A",
            metrics: data.metrics || "N/A",
            sites: data.sites || "N/A",
            products: data.products || "N/A",
        };

        // Crea un objeto URLSearchParams para construir los parámetros de la solicitud POST
        const params = new URLSearchParams();

        // Añade el cuerpo de la solicitud con los datos del incidente y los nombres extraídos
        params.append('payload', JSON.stringify({
            text: `Incident ID(s): ${sanitizedData.id}\nTitle(s): ${sanitizedData.titles}\nMetrics: ${sanitizedData.metrics}\nSites: ${sanitizedData.sites}\nProducts: ${sanitizedData.products}\nNames: ${extractedNames.join(', ') || "N/A"}`
        }));

        // Realiza una solicitud POST a Slack utilizando la URL del webhook
        const response = await fetch(SLACK_WEBHOOK_URL, {
            method: 'POST',
            body: params,
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        });

        // Verifica si la respuesta de Slack es exitosa
        if (!response.ok) {
            throw new Error(`Slack API error: ${response.statusText}`); // Si no es exitosa, lanza un error
        }

        console.log('Data sent to Slack successfully:', sanitizedData); // Si todo va bien, muestra un mensaje de éxito
        sendResponse({ success: true }); // Responde indicando que la operación fue exitosa

    } catch (error) {
        // Si ocurre un error, lo captura y muestra en la consola
        console.error('Error sending to Slack:', error);

        // Responde indicando que hubo un error, junto con el mensaje del error
        sendResponse({ success: false, error: error.message });
    }
}






















































