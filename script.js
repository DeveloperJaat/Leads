function search() {
    let query = document.getElementById("searchQuery").value;
    fetch("/search?query=" + encodeURIComponent(query))
        .then(response => response.json())
        .then(data => {
            let resultsDiv = document.getElementById("results");
            resultsDiv.innerHTML = "";
            data.results.forEach(result => {
                resultsDiv.innerHTML += `<p><a href="${result.link}" target="_blank">${result.title}</a></p>`;
            });
        })
        .catch(error => console.log("Error:", error));
}
