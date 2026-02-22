/*
 * JavaScript del proyecto
 * Por ahora solo confirmación al desmarcar favoritos
 */

document.addEventListener('DOMContentLoaded', function() {
    // Confirmar antes de quitar de favoritos
    const favoriteButtons = document.querySelectorAll('form[action*="toggle-favorite"] button');
    
    favoriteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Si tiene la estrella llena (es favorita)
            if (this.textContent.includes('★')) {
                // Pregunto antes de quitar
                if (!confirm('¿Quitar de favoritas?')) {
                    e.preventDefault();
                }
            }
        });
    });
});