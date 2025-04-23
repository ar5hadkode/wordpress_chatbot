const widgetBtn = document.createElement("button");
widgetBtn.innerText = "💬 Chat";
widgetBtn.className = "chat-widget-btn";
document.body.appendChild(widgetBtn);


const widgetBox = document.createElement("div");
widgetBox.className = "chat-widget-box";
document.body.appendChild(widgetBox);

widgetBox.innerHTML = `
  <div class="chat-header">
    <svg xmlns="http://www.w3.org/2000/svg" class="chat-icon" viewBox="0 0 24 24" fill="white" width="24" height="24">
      <path d="M4 4h16v12H5.17L4 17.17V4zm0-2c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4a2 2 0 0 0-2-2H4z"/>
    </svg>
    <span>Chat with Us</span>
  </div>
  <div class="chat-window">
    <div class="messages"></div>
  </div>
  <form id="user-form">
    <input type="text" id="first-name" placeholder="First Name" required />
    <input type="text" id="last-name" placeholder="Last Name" required />
    <input type="number" id="age" placeholder="Age" required min="1" />
    <input type="email" id="email" placeholder="Your Email" required />
    <input type="text" id="phone" placeholder="Your Phone" required />
    <button type="submit">Start Chat</button>
  </form>
  <form id="chat-form" style="display:none;">
    <input type="text" id="message-input" placeholder="Type your message..." required />
    <button type="submit">Send</button>
  </form>
`;

widgetBtn.onclick = () => {
  widgetBox.style.display = widgetBox.style.display === "none" ? "block" : "none";
};

let userData = {};

document.getElementById("user-form").onsubmit = async (e) => {
  e.preventDefault();
  userData = {
    firstName: document.getElementById("first-name").value.trim(),
    lastName: document.getElementById("last-name").value.trim(),
    age: document.getElementById("age").value.trim(),
    email: document.getElementById("email").value.trim(),
    phone: document.getElementById("phone").value.trim(),
  };

  await fetch(`${API_URL}/user-info`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(userData),
  });

  document.getElementById("user-form").style.display = "none";
  document.getElementById("chat-form").style.display = "flex";
};

document.getElementById("chat-form").onsubmit = async (e) => {
  e.preventDefault();
  const input = document.getElementById("message-input");
  const msg = input.value.trim();
  if (!msg) return;

  addMessage("user", msg);
  input.value = "";

  const res = await fetch(`${API_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: msg, ...userData })
  });

  const data = await res.json();

  if (data.reply) {
    addMessage("bot", data.reply);
  } else {
    addMessage("bot", "Sorry, something went wrong. Please try again.");
  }
};

function addMessage(role, text) {
  const msg = document.createElement("div");
  msg.className = "msg " + role;
  msg.innerText = text;
  document.querySelector(".messages").appendChild(msg);
  document.querySelector(".chat-window").scrollTop = 99999;
}
