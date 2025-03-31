document.addEventListener('DOMContentLoaded', function() {
    const nameList = document.getElementById('nameList');
    const searchBox = document.getElementById('searchBox');
    const incidentList = document.getElementById('incidentList');
    const sendToSlackBtn = document.getElementById('sendToSlackBtn');
    const clearNamesBtn = document.getElementById('clearNamesBtn');

    // Inicializar nombres y temporizadores al cargar
    loadStoredNames();
    fetchAndDisplayIncidents();
    setTimerInterval();

    // Filtrar nombres al escribir en el cuadro de búsqueda
    searchBox.addEventListener('input', filterNames);

    clearNamesBtn.addEventListener('click', clearNames);

    sendToSlackBtn.addEventListener('click', handleSlackSend);

    function loadStoredNames() {
        chrome.storage.local.get(['participantNames'], function(result) {
            const storedNames = result.participantNames || [];
            displayNames(storedNames);
        });
    }

    function displayNames(names) {
        nameList.innerHTML = '';
        if (names.length === 0) {
            nameList.innerHTML = '<p>No hay nombres disponibles.</p>';
            return;
        }

        // Usar fragment para minimizar el acceso al DOM
        const fragment = document.createDocumentFragment();
        names.forEach(name => {
            const listItem = document.createElement('li');
            listItem.className = 'name-item';
            listItem.innerHTML = `
                <label>${name}</label>
                <span id="timer-${name}" class="timer">${formatTime(0)}</span>
            `;
            fragment.appendChild(listItem);
        });
        nameList.appendChild(fragment);
    }

    function filterNames() {
        const filter = searchBox.value.toLowerCase();
        const names = document.querySelectorAll('.name-item');
        names.forEach(nameItem => {
            const text = nameItem.querySelector('label').textContent.toLowerCase();
            nameItem.style.display = text.includes(filter) ? '' : 'none';
        });
    }

    function clearNames() {
        chrome.storage.local.remove(['participantNames', 'timers'], function() {
            nameList.innerHTML = '<p>No hay nombres disponibles.</p>';
            console.log('Nombres y temporizadores eliminados.');
        });
    }

    function setTimerInterval() {
        setInterval(() => {
            chrome.storage.local.get(['timers'], function(result) {
                const timers = result.timers || {};
                updateTimers(timers);
            });
        }, 1000); // Puede ser ajustado según sea necesario
    }

    function updateTimers(timers) {
        document.querySelectorAll('.timer').forEach(timer => {
            const name = timer.id.replace('timer-', '');
            const elapsed = timers[name] ? timers[name].elapsed : 0;
            timer.textContent = formatTime(elapsed);
        });
    }

    function formatTime(seconds) {
        const minutes = String(Math.floor(seconds / 60)).padStart(2, '0');
        const secs = String(seconds % 60).padStart(2, '0');
        return `${minutes}:${secs}`;
    }

    function fetchAndDisplayIncidents() {
        fetch('https://sme-panic-button.adminml.com/get_incident')
            .then(response => response.json())
            .then(data => {
                if (!data || !Array.isArray(data) || data.length === 0) {
                    incidentList.innerHTML = `<p>No hay incidentes disponibles.</p>`;
                    return;
                }

                const incidents = data.map(item => item.incident);
                // Usar fragment para minimizar el acceso al DOM
                const fragment = document.createDocumentFragment();
                incidents.forEach(incident => {
                    const { id_pb, title, metrics, sites, products } = incident.data;
                    const button = document.createElement('button');
                    button.className = 'incident-btn';
                    button.dataset.id = id_pb;
                    button.dataset.title = title || '';
                    button.dataset.metrics = metrics?.join(', ') || '';
                    button.dataset.sites = sites?.join(', ') || '';
                    button.dataset.products = products?.join(', ') || '';
                    button.textContent = id_pb;

                    const div = document.createElement('div');
                    div.className = 'incident-item';
                    div.appendChild(button);

                    fragment.appendChild(div);
                });
                incidentList.innerHTML = ''; // Limpiar antes de agregar nuevos elementos
                incidentList.appendChild(fragment);

                addIncidentButtonListeners();
            })
            .catch(error => {
                console.error('Error al obtener o mostrar incidentes:', error);
                incidentList.innerHTML = `<p>Error al cargar incidentes.</p>`;
            });
    }

    function addIncidentButtonListeners() {
        incidentList.addEventListener('click', function(event) {
            if (event.target.classList.contains('incident-btn')) {
                event.target.classList.toggle('selected');
            }
        });
    }

    function handleSlackSend() {
        const selectedButtons = document.querySelectorAll('.incident-btn.selected');
        if (selectedButtons.length === 0) {
            alert('Selecciona al menos un incidente antes de enviar a Slack.');
            return;
        }

        const combinedData = Array.from(selectedButtons).reduce((acc, button) => {
            acc.id.push(button.dataset.id);
            acc.title.push(button.dataset.title);
            acc.metrics.push(button.dataset.metrics);
            acc.sites.push(button.dataset.sites);
            acc.products.push(button.dataset.products) || '';
            return acc;
        }, { id: [], title: [], metrics: [], sites: [], products: [] });

        const combinedId = combinedData.id.join('-');
        const combinedTitle = combinedData.title.join(' / ');
        const combinedMetrics = combinedData.metrics.join(', ');
        const combinedSites = combinedData.sites.join(', ');
        const combinedProducts = combinedData.products.join(', ');

        sendToSlack(combinedId, combinedTitle, combinedMetrics, combinedSites, combinedProducts);
    }

    function sendToSlack(id, titles, metrics, sites, products) {
        chrome.storage.local.get(['timers'], function(result) {
            const timers = result.timers || {};
            const extractedNames = Object.keys(timers).filter(name => timers[name].elapsed > 0);

            if (extractedNames.length === 0) {
                alert('No hay nombres con tiempo registrado para enviar a Slack.');
                return;
            }

            chrome.runtime.sendMessage({
                type: 'sendToSlack',
                data: {
                    id,
                    titles,
                    metrics,
                    products,
                    sites,
                    extractedNames
                }
            }, response => {
                if (response && response.success) {
                    alert('¡Mensaje enviado correctamente!');
                } else {
                    alert('Error al enviar el mensaje a Slack.');
                }
            });
        });
    }
});






















































































  