document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("scrapeForm");
    const message = document.getElementById("message");
    const downloadLink = document.getElementById("downloadLink");

    form.addEventListener("submit", function(event) {
        event.preventDefault();  // Prevent page reload

        const query = document.getElementById("query").value;
        message.innerHTML = "Scraping in progress...";

        fetch("/scrape", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query: query })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                message.innerHTML = `<span style="color: red;">Error: ${data.error}</span>`;
            } else {
                message.innerHTML = `Scraping Complete! Found ${data.total_leads} leads.`;
                downloadLink.style.display = "block";
            }
        })
        .catch(error => {
            message.innerHTML = `<span style="color: red;">Error: ${error}</span>`;
        });
    });
});
