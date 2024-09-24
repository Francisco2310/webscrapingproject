document.getElementById('download-link').addEventListener('click', function(event) {
    event.preventDefault();
    const link = document.createElement('a');
    link.href = '/excel';
    link.download = 'temp_arquivo.xlsx';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
});
