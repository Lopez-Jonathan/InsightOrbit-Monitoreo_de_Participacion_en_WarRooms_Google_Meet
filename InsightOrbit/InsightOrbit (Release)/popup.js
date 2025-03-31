document.addEventListener('DOMContentLoaded', function() {
    const nameList = document.getElementById('nameList');
    const searchBox = document.getElementById('searchBox');
    const incidentList = document.getElementById('incidentList');

    chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
        if (message.type === 'closeTab' && message.action === 'executeHandleSlackSend') {
            // Ejecutar la función handleSlackSend cuando se reciba el mensaje
            handleSlackSend();
        }
    });

    // Inicializar nombres y temporizadores al cargar
    loadStoredNames();
    fetchAndDisplayIncidents();
    setTimerInterval();

    // Filtrar nombres al escribir en el cuadro de búsqueda
    searchBox.addEventListener('input', filterNames);

    // Función que carga los nombres almacenados desde el almacenamiento local de Chrome
    function loadStoredNames() {
        // Se utiliza chrome.storage.local.get para obtener los datos almacenados bajo la clave 'participantNames'
        chrome.storage.local.get(['participantNames'], function(result) {
            // Si 'participantNames' existe en el almacenamiento, se toma su valor. Si no, se asigna un arreglo vacío por defecto.
            const storedNames = result.participantNames || [];

            // Llamamos a la función displayNames con el arreglo de nombres almacenados para mostrar los nombres
            displayNames(storedNames);
        });
    }

    // Función para mostrar los nombres de los participantes en una lista
    function displayNames(names) {
        // Primero, vaciar el contenido de la lista de nombres (esto elimina los elementos previos)
        nameList.innerHTML = '';

        // Si no hay nombres en el arreglo, se muestra un mensaje indicando que no hay nombres disponibles
        if (names.length === 0) {
            nameList.innerHTML = '<p>No hay nombres disponibles.</p>';
            return; // Salir de la función si no hay nombres para mostrar
        }

        // Crear un fragmento de documento para minimizar el acceso al DOM y mejorar el rendimiento
        const fragment = document.createDocumentFragment();

        // Iterar sobre el arreglo de nombres y crear un elemento de lista <li> para cada uno
        names.forEach(name => {
            const listItem = document.createElement('li'); // Crear un nuevo elemento <li>
            listItem.className = 'name-item'; // Asignar la clase 'name-item' al <li> para estilos

            // Establecer el contenido HTML del <li> con el nombre del participante y un temporizador inicial
            listItem.innerHTML = `
                <label>${name}</label> <!-- Mostrar el nombre -->
                <span id="timer-${name}" class="timer">${formatTime(0)}</span> <!-- Mostrar el temporizador con tiempo inicial formateado -->
            `;

            // Añadir el <li> al fragmento de documento
            fragment.appendChild(listItem);
        });

        // Al final, añadir todo el fragmento de una vez al DOM (esto es más eficiente que añadir cada elemento individualmente)
        nameList.appendChild(fragment);
    }

    // Función para filtrar los nombres basados en la búsqueda ingresada en el cuadro de búsqueda (searchBox)
    function filterNames() {
        // Obtener el valor del cuadro de búsqueda (searchBox) y convertirlo a minúsculas para realizar una búsqueda insensible a mayúsculas/minúsculas
        const filter = searchBox.value.toLowerCase();

        // Obtener todos los elementos con la clase 'name-item' (suponiendo que son los elementos de la lista de nombres)
        const names = document.querySelectorAll('.name-item');

        // Iterar sobre cada elemento de la lista de nombres
        names.forEach(nameItem => {
            // Obtener el texto dentro del <label> de cada elemento de la lista, convertirlo a minúsculas
            const text = nameItem.querySelector('label').textContent.toLowerCase();

            // Comprobar si el texto del nombre contiene el filtro ingresado en el cuadro de búsqueda
            // Si el nombre contiene el filtro, se muestra el elemento (display = '')
            // Si no, se oculta el elemento (display = 'none')
            nameItem.style.display = text.includes(filter) ? '' : 'none';
        });
    }

    // Función que configura un intervalo para actualizar los temporizadores cada cierto tiempo
    function setTimerInterval() {
        // setInterval ejecuta una función repetidamente en un intervalo de tiempo especificado (1000 ms = 1 segundo)
        setInterval(() => {
            // Obtener el objeto 'timers' almacenado en chrome.storage.local
            chrome.storage.local.get(['timers'], function(result) {
                // Si no se encuentran temporizadores en el almacenamiento, inicializa un objeto vacío
                const timers = result.timers || {};

                // Llamar a la función updateTimers para actualizar la interfaz o los datos con los temporizadores
                updateTimers(timers);
            });
        }, 1000); // El intervalo está configurado en 1000 ms (1 segundo), pero puede ajustarse a cualquier valor necesario
    }

    // Función que actualiza la visualización de los temporizadores en la interfaz
    function updateTimers(timers) {
        // Recorre todos los elementos con la clase 'timer' (que son los temporizadores visibles en la UI)
        document.querySelectorAll('.timer').forEach(timer => {
            // Extrae el nombre del participante del 'id' del temporizador (el id tiene el formato 'timer-nombre')
            const name = timer.id.replace('timer-', ''); // Elimina el prefijo 'timer-' para obtener el nombre del participante

            // Recupera el tiempo transcurrido del objeto 'timers' asociado con el nombre del participante
            // Si no existe un temporizador para ese nombre, se asigna 0 como valor por defecto
            const elapsed = timers[name] ? timers[name].elapsed : 0;

            // Actualiza el contenido del temporizador en la UI con el tiempo formateado
            timer.textContent = formatTime(elapsed);
        });
    }

    // Función para formatear el tiempo en formato 'MM:SS' (minutos:segundos)
    function formatTime(seconds) {
        // Calcula los minutos dividiendo los segundos entre 60 y redondeando hacia abajo
        // Luego convierte el número de minutos a una cadena de texto y le asegura tener al menos 2 dígitos
        const minutes = String(Math.floor(seconds / 60)).padStart(2, '0');

        // Calcula los segundos restantes (el residuo de la división entre 60)
        // Luego convierte el número de segundos a una cadena de texto y le asegura tener al menos 2 dígitos
        const secs = String(seconds % 60).padStart(2, '0');

        // Devuelve el tiempo formateado como 'MM:SS'
        return `${minutes}:${secs}`;
    }


    // Función para obtener e mostrar incidentes desde una API
    function fetchAndDisplayIncidents() {
        // Realiza una solicitud GET a la primera API de incidentes
        fetch('URL_TICKETERA1')
            .then(response => response.json())  // Convierte la respuesta a formato JSON
            .then(data => {
                // Verifica si los datos obtenidos son válidos (una lista no vacía)
                if (!data || !Array.isArray(data) || data.length === 0) {
                    // Si no hay incidentes, muestra un mensaje adecuado
                    incidentList.innerHTML = `<p>No hay incidentes disponibles.</p>`;
                } else {
                    // Extrae los incidentes de los datos recibidos
                    const incidents = data.map(item => item.incident);

                    // Usar un fragmento de documento para minimizar el acceso al DOM
                    const fragment = document.createDocumentFragment();

                    // Itera sobre cada incidente y crea un botón para cada uno
                    incidents.forEach(incident => {
                        const { id_pb, title, metrics, sites, products } = incident.data;

                        // Crea un botón para el incidente
                        const button = document.createElement('button');
                        button.className = 'incident-btn';  
                        button.dataset.id = id_pb;  
                        button.dataset.title = title || '';  
                        button.dataset.metrics = metrics?.join(', ') || '';  
                        button.dataset.sites = sites?.join(', ') || '';  
                        button.dataset.products = products?.join(', ') || '';  
                        button.textContent = id_pb;  

                        // Crea un contenedor para el botón (div)
                        const div = document.createElement('div');
                        div.className = 'incident-item';  
                        div.appendChild(button);  

                        // Añade el contenedor al fragmento del documento
                        fragment.appendChild(div);
                    });

                    // Limpia la lista de incidentes antes de agregar nuevos elementos
                    incidentList.innerHTML = '';
                    incidentList.appendChild(fragment);

                    // Llama a una función para añadir event listeners a los botones creados
                    addIncidentButtonListeners();

                    // Restaura el estado de los botones (seleccionados/desmarcados)
                    restoreButtonState();
                }
            })
            .catch(error => {
                console.error('Error al obtener o mostrar incidentes:', error);
                incidentList.innerHTML = `<p>Error al cargar incidentes.</p>`;
            })
            /*.finally(() => {
                // Realiza la solicitud GET a la segunda API con autenticación (cookies de sesión)
                fetch('URL_TICKETERA2', {
                    method: 'GET',  // Método GET
                    credentials: 'same-origin',  // Enviar cookies de sesión con la solicitud
                    headers: {
                        'Accept': 'application/json'  // Asegúrate de que la respuesta sea en formato JSON
                    }
                })
                .then(response => {
                    // Verifica si la respuesta no es un error HTML (que podría ser una página de login o un error)
                    console.log('Respuesta de Moody:', response);
                    
                    // Si la respuesta es HTML, probablemente sea una página de error o de inicio de sesión
                    return response.text();  // Lee la respuesta como texto en lugar de JSON
                })
                .then(responseText => {
                    console.log('Texto de la respuesta:', responseText);  // Muestra el contenido de la respuesta
                    try {
                        // Intenta analizar el contenido como JSON
                        const data = JSON.parse(responseText);
                        console.log('Incidentes desde Moody:', data);
                        if (data && Array.isArray(data)) {
                            // Procesa los incidentes aquí
                        } else {
                            console.log('No se encontraron incidentes en la API de Moody.');
                        }
                    } catch (error) {
                        // Si la respuesta no es JSON, muestra un error y el contenido HTML que se recibió
                        console.error('Error al analizar la respuesta JSON:', error);
                        console.error('Contenido de la respuesta:', responseText);
                    }
                })
                .catch(error => {
                    // Maneja cualquier error, incluyendo la respuesta no válida
                    console.error('Error al obtener incidentes de Moody:', error);
                });
            });*/
    }


    // Función para añadir listeners (oyentes de eventos) a los botones de incidentes
    function addIncidentButtonListeners() {
        // Añade un evento de clic al contenedor de incidentes (incidentList)
        incidentList.addEventListener('click', function(event) {
            // Verifica si el objetivo del clic (el elemento sobre el que se hizo clic) es un botón de incidente
            if (event.target.classList.contains('incident-btn')) {
                // Cambia el estado de selección del botón, alternando la clase 'selected'
                // Si el botón ya tiene la clase 'selected', se eliminará; si no, se añadirá
                event.target.classList.toggle('selected');
            
                // Obtiene todos los botones que tienen la clase 'selected' (los botones seleccionados)
                const selectedButtons = document.querySelectorAll('.incident-btn.selected');
            
                // Extrae los IDs de los incidentes seleccionados de los botones seleccionados
                // Se utiliza `Array.from` para convertir la lista de nodos en un array, luego se mapean los botones para obtener solo los IDs
                const selectedIds = Array.from(selectedButtons).map(button => button.dataset.id);
            
                // Almacena los IDs de los incidentes seleccionados en `chrome.storage.local`
                // Esto asegura que la selección persista incluso si la página se recarga
                chrome.storage.local.set({ selectedIncidents: selectedIds });
            }
        });
    }
    
    // Función para restaurar el estado de los botones de incidentes seleccionados
    function restoreButtonState() {
        // Obtener los IDs de los botones seleccionados desde el almacenamiento local de Chrome
        // Se accede a chrome.storage.local para obtener el array de IDs previamente almacenados
        chrome.storage.local.get('selectedIncidents', function(result) {
            // Si no hay incidentes seleccionados guardados, se inicializa como un array vacío
            const selectedIds = result.selectedIncidents || [];
    
            // Seleccionar todos los botones de incidentes presentes en la página
            const buttons = document.querySelectorAll('.incident-btn');
        
            // Recorrer todos los botones de incidentes
            buttons.forEach(button => {
                // Verificar si el ID del incidente en el botón está en la lista de IDs seleccionados
                if (selectedIds.includes(button.dataset.id)) {
                    // Si el botón está en la lista de seleccionados, añadir la clase 'selected' para marcarlo
                    button.classList.add('selected');
                }
            });
        });
    }


    // Llama a restoreButtonState cuando se abre la extensión
    document.addEventListener('DOMContentLoaded', restoreButtonState);
    
    // Función para manejar el envío de datos a Slack
    function handleSlackSend() {
        // Obtener todos los botones de incidentes que están seleccionados
        const selectedButtons = document.querySelectorAll('.incident-btn.selected');
        
        // Si no hay botones seleccionados, responder con éxito y detener ejecución
        if (selectedButtons.length === 0) {
            chrome.runtime.sendMessage({ success: true }, () => {
                console.log("No hay incidentes seleccionados. Continuando el flujo...");
            });
        }
    
        // Combinar los datos de los botones seleccionados
        const combinedData = Array.from(selectedButtons).reduce((acc, button) => {
            acc.id.push(button.dataset.id);
            acc.title.push(button.dataset.title);
            acc.metrics.push(button.dataset.metrics);
            acc.sites.push(button.dataset.sites);
            acc.products.push(button.dataset.products || '');
            return acc;
        }, { id: [], title: [], metrics: [], sites: [], products: [] });
    
        // Preparar datos combinados
        const combinedId = combinedData.id.join('-');
        const combinedTitle = combinedData.title.join(' / ');
        const combinedMetrics = combinedData.metrics.join(', ');
        const combinedSites = combinedData.sites.join(', ');
        const combinedProducts = combinedData.products.join(', ');
    
        // Almacenar datos combinados y llamar a sendToSlack
        chrome.storage.local.set({
            slackData: {
                id: combinedId,
                titles: combinedTitle,
                metrics: combinedMetrics,
                sites: combinedSites,
                products: combinedProducts
            }
        }, () => {
            sendToSlack(combinedId, combinedTitle, combinedMetrics, combinedSites, combinedProducts)
                .then(() => {
                    chrome.runtime.sendMessage({ success: true }, () => {
                        console.log("Datos enviados a Slack correctamente.");
                    });
                })
                .catch(error => {
                    console.error("Error al enviar datos a Slack:", error);
                    chrome.runtime.sendMessage({ success: false }, () => {
                        console.warn("Fallo en Slack, pero se continúa.");
                    });
                });
        });
    }

    // Función para enviar los datos a Slack
    function sendToSlack(id, titles, metrics, sites, products) {
        return new Promise((resolve, reject) => {
            // Obtener los temporizadores almacenados en chrome.storage.local
            chrome.storage.local.get(['timers'], function(result) {
                const timers = result.timers || {}; // Si no hay temporizadores, usar un objeto vacío
                // Filtrar los nombres de los temporizadores que tienen tiempo registrado
                const extractedNames = Object.keys(timers).filter(name => timers[name].elapsed > 0);

                // Si no hay nombres con tiempo registrado, mostrar un mensaje y rechazar la promesa
                if (extractedNames.length === 0) {
                    alert('No hay nombres con tiempo registrado para enviar a Slack.'); // Alerta al usuario
                    reject('No hay nombres con tiempo registrado.'); // Rechazar la promesa con un mensaje
                    return;
                }

                // Enviar los datos a Slack utilizando chrome.runtime.sendMessage
                chrome.runtime.sendMessage({
                    type: 'sendToSlack', // Tipo de mensaje que indica que es un envío a Slack
                    data: {
                        id,               // ID de los incidentes
                        titles,           // Títulos de los incidentes
                        metrics,          // Métricas de los incidentes
                        products,         // Productos relacionados
                        sites,            // Sitios afectados
                        extractedNames    // Nombres extraídos con tiempo registrado
                    }
                }, response => {
                    // Manejar la respuesta de la operación de envío
                    if (response && response.success) {
                        // alert('¡Mensaje enviado correctamente!'); // Mostrar mensaje de éxito
                        resolve('Mensaje enviado correctamente'); // Resolver la promesa con un mensaje de éxito
                    } else {
                        alert('Error al enviar el mensaje a Slack.'); // Mostrar mensaje de error
                        reject('Error al enviar el mensaje'); // Rechazar la promesa con un mensaje de error
                    }
                });
            });
        });
    }

});






















































































  
