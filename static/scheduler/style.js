function handleDateValidation(event){
    var endTime = document.getElementById("endTime").value;
    var startTime = document.getElementById("startTime").value;
    var error = document.getElementById("error");
    
    if(endTime < startTime){
         error.textContent = "End time should be after the start time of the interview.";
         error.style.color = "red";
         event.preventDefault();
     } 
     else {
         error.textContent = "";
     }
     
     return false;
}

let count = 2;
function addParticipant(){
    // Get the element where the inputs will be added to
    let container = document.getElementById("container");
    
    // Count of already present nodes
    count += 1;

    // Creating new element
    let newDiv = document.createElement("div");

    let tmpClassName = "participant"
    tmpClassName += count
    newDiv.className += tmpClassName

    // Append a node with label text
    newLabel = document.createElement("label");
    newLabel.innerHTML = "Participant Mail";
    newLabel.setAttribute("class", "block text-base mb-2")

    // New child div
    let newChildDiv = document.createElement("div")
    newChildDiv.setAttribute("class", "flex")
    
    // Create an <input> element, set its type and name attributes
    let newInput = document.createElement("input");

    newInput.type = "email";
    newInput.name = "email";
    newInput.placeholder = "Mail Address"
    newInput.setAttribute("class","flex-1 bg-gray-50 border border-gray-300 text-slate-700 text-sm rounded-l-lg focus:border-blue-500 block w-full p-2.5");
    
    //
    let newSpan = document.createElement("span")
    newSpan.textContent = "X"
    newSpan.setAttribute("class", "cursor-default bg-gray-200 inline-flex items-center px-3 text-sm text-gray-900 rounded-r-lg border border-l-0 border-gray-300")
    newSpan.setAttribute("id", tmpClassName)
    newSpan.setAttribute("onclick", "removeParent(this)")


    // Appending span and input into the child div
    newChildDiv.appendChild(newInput);
    newChildDiv.appendChild(newSpan)

    // Appending child div and label into new div
    newDiv.append(newLabel)
    newDiv.appendChild(newChildDiv)
    
    // Appending new div into the parent node
    container.appendChild(newDiv);
}