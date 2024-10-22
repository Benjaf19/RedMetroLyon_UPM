document.addEventListener("DOMContentLoaded", function() {
  const metroImage = document.getElementById("metroImage");
  metroImage.addEventListener("click", handleClick);

  let estacionIda = "";
  let estacionDestino = "";

 const estacionesCoordenadas = {
  "Perrache": { x: 230, y: 324, radio: 30 },
  "Ampère Victor Hugo": { x: 251, y: 292, radio: 30 },
  "Cordeliers": { x: 296, y: 216, radio: 15 },
  "Foch": { x: 351, y: 178, radio: 30 },
  "Masséna": { x: 408, y: 173, radio: 30 },
  "République Villeurbanne": { x: 543, y: 163, radio: 30 },
  "Gratte-Ciel": { x: 599, y: 175, radio: 30 },
  "Flachet": { x: 648, y: 187, radio: 30 },
  "Cusset": { x: 715, y: 202, radio: 30 },
  "Laurent Bonnevay Astroballe": { x: 772, y: 206, radio: 30 },
  "Vaulx-en-Velin La Soie": { x: 858, y: 234, radio: 30 },
  "Oullins Gare": { x: 150, y: 560, radio: 30 },
  "Stade de Gerland": { x: 259, y: 480, radio: 30 },
  "Debourg": { x: 280, y: 447, radio: 30 },
  "Place Jean Jaurès": { x: 306, y: 397, radio: 30 },
  "Jean Macé": { x: 338, y: 343, radio: 30 },
  "Place Guichard Bourse du Travail": { x: 371, y: 243, radio: 30 },
  "Gare Part-Dieu Vivier Merle": { x: 438, y: 231, radio: 30 },
  "Brotteaux": { x: 446, y: 192, radio: 30 },
  "Cuire": { x: 279, y: 54, radio: 30 },
  "Henon": { x: 241, y: 103, radio: 30 },
  "Croix-Rousse": { x: 269, y: 138, radio: 30 },
  "Croix-Paquet": { x: 298, y: 162, radio: 15 },
  "Gare de Vaise": { x: 98, y: 91, radio: 30 },
  "Valmy": { x: 97, y: 134, radio: 30 },
  "Gorge de Loup": { x: 91, y: 197, radio: 30 },
  "Vieux Lyon Cathédrale St. Jean": { x: 228, y: 241, radio: 30 },
  "Guillotière": { x: 335, y: 271, radio: 30 },
  "Garibaldi": { x: 412, y: 299, radio: 30 },
  "Sans-Souci": { x: 483, y: 325, radio: 30 },
  "Monplaisir-Lumière": { x: 528, y: 343, radio: 30 },
  "Grange Blanche": { x: 575, y: 363, radio: 30 },
  "Laënnec": { x: 624, y: 395, radio: 30 },
  "Mermoz Pinel": { x: 629, y: 452, radio: 30 },
  "Parilly": { x: 619, y: 532, radio: 30 },
  "Gare de Vénissieux": { x: 634, y: 628, radio: 30 },
  "Bellecour": { x: 281, y: 256, radio: 30 },
  "Hôtel de Ville Louis Pradel": { x: 296, y: 186, radio: 15 },
  "Charpennes Charles Hernu": { x: 472, y: 163, radio: 30 },
  "Saxe Gambetta": { x: 367, y: 284, radio: 30 }
};


const limpiarBoton = document.getElementById("limpiarBoton");
limpiarBoton.addEventListener("click", limpiarCampos);

 function handleClick(event) {
    const rect = metroImage.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    const estacionSeleccionada = getEstacionPorCoordenadas(x, y);

    if (estacionIda === "") {
      estacionIda = estacionSeleccionada;
      document.getElementById("estacion_origen").value = estacionIda;
    } else if (estacionDestino === "" && estacionSeleccionada !== estacionIda) {
      estacionDestino = estacionSeleccionada;
      document.getElementById("estacion_destino").value = estacionDestino;
    }
  }

  function getEstacionPorCoordenadas(x, y) {
    for (const estacion in estacionesCoordenadas) {
      const { x: estacionX, y: estacionY, radio: estacionRadio } = estacionesCoordenadas[estacion];
      if (isInsideArea(x, y, estacionX, estacionY, estacionRadio)) {
        return estacion;
      }
    }
    return "";
  }

  function isInsideArea(x, y, centerX, centerY, radius) {
    const distance = Math.sqrt((x - centerX) ** 2 + (y - centerY) ** 2);
    return distance <= radius;
  }
  function limpiarCampos() {
    estacionIda = "";
    estacionDestino = "";
    document.getElementById("estacion_origen").value = "";
    document.getElementById("estacion_destino").value = "";
  }
});
