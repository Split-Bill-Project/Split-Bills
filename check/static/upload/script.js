document.getElementById("groupForm").addEventListener("submit", function(event) {
    event.preventDefault();
  
    const groupName = document.getElementById("groupName").value;
    fetch("/get_column_names", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        groupName: groupName
      })
    })
    .then(response => response.json())
    .then(data => {
      const columnForm = document.getElementById("columnForm");
      columnForm.innerHTML = ""; // Clear previous radio buttons
  
      // Create radio buttons for each column name
      data.columnNames.forEach(function(columnName) {
        const label = document.createElement("label");
        label.textContent = columnName;
  
        const radioButton = document.createElement("input");
        radioButton.type = "radio";
        radioButton.name = "column";
        radioButton.value = columnName;
  
        columnForm.appendChild(label);
        columnForm.appendChild(radioButton);
        columnForm.appendChild(document.createElement("br"));
      });
  
      document.getElementById("columnNames").style.display = "block";
    });
  });
  
  document.getElementById("columnForm").addEventListener("submit", function(event) {
    event.preventDefault();
  
    const selectedColumn = document.querySelector('input[name="column"]:checked').value;
    // You can send the selected column to the backend or perform any other desired action
  });
  