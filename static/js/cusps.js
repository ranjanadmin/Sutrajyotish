async function loadCusps() {
  const res = await fetch("/api/cusps");
  const data = await res.json();

  const tbody = document.getElementById("cuspTable");
  tbody.innerHTML = "";

  data.forEach(row => {
    const tr = document.createElement("tr");

    tr.innerHTML = `
      <td>${row.hs}</td>
      <td>${row.sign}</td>
      <td>${row.degree}</td>
      <td>${row.lord}</td>
      <td>${row.nak}</td>
      <td>${row.sub}</td>
      <td>${row.ssub}</td>
    `;

    tbody.appendChild(tr);
  });
}

loadCusps();