// confirmar.js
// Utilidad mínima para confirmar acciones destructivas en formularios
// Se enlaza desde plantillas en botones de eliminar (onsubmit -> return confirmarEliminacion()).
function confirmarEliminacion(){
    return confirm('¿Deseas eliminar este registro?');
}
