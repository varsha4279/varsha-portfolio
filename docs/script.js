
const contactForm = document.getElementById("contactForm");
const response = document.getElementById("response");

contactForm.addEventListener("submit", async function(event) {

    event.preventDefault();

    const contactData = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        message: document.getElementById("message").value
    };

    try {
        const result = await fetch("/api/contact", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(contactData)
        });

        const data = await result.json();

        if (!result.ok) {
            throw new Error(data.error || "Something went wrong");
        }

        response.innerText = data.message;
        response.style.color = "green";
        contactForm.reset();

    } catch (error) {
        response.innerText = error.message;
        response.style.color = "red";
    }

});
