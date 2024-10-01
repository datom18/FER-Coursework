
increment = (itemName) => {
    let counter = document.getElementById(itemName);
    if(isNaN(parseInt(counter.textContent))){
       counter.textContent = 1;
    }
    else{
       counter.textContent++;
    }
 
    let counterTotal = document.getElementById("cartAmount");
    if(isNaN(parseInt(counterTotal.textContent))){
       counterTotal.textContent = 1;
    }
    else{
        counterTotal.textContent++;
    }
}

decrement = (itemName) => {
    let counter = document.getElementById(itemName);
    if(counter.textContent > 1){
        counter.textContent--;
    }
    else if(counter.textContent == 1){
        let quantityDOM = document.getElementById(`values-${itemName}`);
        let itemDOM = document.getElementById(`added-items-${itemName}`);
        quantityDOM.remove();
        itemDOM.remove();
    }

    let counterTotal = document.getElementById("cartAmount");
    if(counterTotal.textContent > 1){
        counterTotal.textContent--;
    }

    else if(counterTotal.textContent == 1){
        counterTotal.textContent = 0;

        let main = document.getElementById("main");
        main.remove();
        let container = document.getElementById("container");
        container.innerHTML +=
        `
        <div id="main-empty" class="main-empty">
            <h2>Vaša košarica je prazna.</h2>
            <div id="back-home" class="back-home">
            <a href="/">Povratak</a>
            </div>
        </div>
        `;
    }
}
