function searchLeads() {
    let platform = document.getElementById('platform').value;
    let emailFormat = document.getElementById('emailFormat').value;
    let businessType = document.getElementById('businessType').value;
    let location = document.getElementById('location').value;

    if (!platform || !emailFormat || !businessType || !location) {
        alert('Please fill in all fields!');
        return;
    }

    let query = `site:${platform} "${emailFormat}" "${businessType}" "${location}"`;

    fetch("/search", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ query: query })
    })
    .then(response => response.json())
    .then(data => {
        let resultsList = document.getElementById("resultsList");
        resultsList.innerHTML = "";
        data.results.forEach(item => {
            let li = document.createElement("li");
            li.innerHTML = `<a href="${item.link}" target="_blank">${item.title}</a> <br> <strong>Emails:</strong> ${item.emails.join(", ")}`;
            resultsList.appendChild(li);
        });
    })
    .catch(error => console.error("Error fetching leads:", error));
}
