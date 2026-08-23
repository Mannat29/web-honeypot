async function fetchLogs() {
  try {
    const res = await fetch("http://127.0.0.1:8080/api/logs");
    const data = await res.json();

    const tableBody = document.getElementById("logs");
    tableBody.innerHTML = "";

    data.reverse().forEach(log => {
      const row = document.createElement("tr");
      row.classList.add("border-b", "border-gray-700", "hover:bg-gray-700");

      row.innerHTML = `
        <td class="px-4 py-2">${log.timestamp}</td>
        <td class="px-4 py-2">${log.ip}</td>
        <td class="px-4 py-2">${log.path}</td>
        <td class="px-4 py-2">${log.user_agent}</td>
      `;

      tableBody.appendChild(row);
    });
  } catch (err) {
    console.error("Error fetching logs:", err);
  }
}

setInterval(fetchLogs, 3000); // refresh every 3s
fetchLogs();
