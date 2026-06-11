async function loadPlanetary() {
  const res = await fetch("/api/planetary");
  const data = await res.json();

  const tbody = document.getElementById("planetTable");
  tbody.innerHTML = "";

  data.forEach(row => {
    const tr = document.createElement("tr");

    tr.innerHTML = `
      <td>${row.pla}</td>
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

loadPlanetary();