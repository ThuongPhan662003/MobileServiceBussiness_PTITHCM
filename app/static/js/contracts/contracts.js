document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("contract-form");
  const tableBody = document.getElementById("contract-table-body");

  function fetchContracts() {
    fetch("/contracts/get-all")
      .then(res => res.json())
      .then(data => {
        tableBody.innerHTML = "";
        data.forEach(contract => {
          tableBody.innerHTML += `
            <tr>
              <td>${contract.id}</td>
              <td>${contract.name}</td>
              <td>${contract.description}</td>
              <td>
                <button class="btn btn-sm btn-warning" onclick="editContract(${contract.id})">Sửa</button>
                <button class="btn btn-sm btn-danger" onclick="deleteContract(${contract.id})">Xoá</button>
              </td>
            </tr>
          `;
        });
      });
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    const id = document.getElementById("contract_id").value;
    const name = document.getElementById("name").value;
    const description = document.getElementById("description").value;

    const method = id ? "PUT" : "POST";
    const url = id ? `/contracts/${id}` : "/contracts/";
    fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, description }),
    })
      .then(res => res.json())
      .then(() => {
        form.reset();
        fetchContracts();
      });
  });

  window.editContract = function (id) {
    fetch(`/contracts/${id}`)
      .then(res => res.json())
      .then(data => {
        document.getElementById("contract_id").value = data.id;
        document.getElementById("name").value = data.name;
        document.getElementById("description").value = data.description;
      });
  };

  window.deleteContract = function (id) {
    if (confirm("Xác nhận xoá hợp đồng?")) {
      fetch(`/contracts/${id}`, { method: "DELETE" })
        .then(res => res.json())
        .then(() => fetchContracts());
    }
  };

  fetchContracts();
});
