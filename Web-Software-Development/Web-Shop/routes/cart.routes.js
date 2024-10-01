
const express = require("express");
const router = express.Router();
const path = require("path");

itemInCart = (cart, name) => {
    for(let i = 0; i < cart.length; i++){
       if(cart[i].name == name){
          return true;
       }
    }
    return false;
}

calculateQuantity = (cart, req) => {
    let total = 0;
    for(let i = 0; i < cart.length; i++){
       total = parseInt(total) + parseInt(cart[i].quantity);
    }
 
    req.session.total = total;
    return total;
 }


router.get("/", (req, res) => {
    res.redirect("/cart/getAll");
})

router.get("/getAll", (req, res) => {

    let cart = req.session.cart;
    let total = req.session.total;

    res.render('cart', {
        cart: cart,
        total: total
    })

})


router.post("/add/:id", (req, res) => {

    let cart;
    let name = req.params.id.toString();
    let quantity = req.body.quantity;
    let item = {name: name, quantity: quantity};  

    if (req.session.cart) {
        cart = req.session.cart;
        if (!itemInCart(cart, name)) {
            cart.push(item);
        }
        else {
            cart.find(it => it.name === item.name).quantity++;
        }
    }
    else {
        req.session.cart = [];
        req.session.cart.push(item);
        cart = req.session.cart;
    }

    calculateQuantity(cart, req);

    return res.sendStatus(204);

})

router.post("/remove/:id", (req, res) => {

    let cart = req.session.cart;
    let total = req.session.total;
    let name = req.params.id;
    let quantity = req.body.quantity;
    let item = {name: name, quantity: quantity};

    let index = cart.findIndex(item => item.name === name);

    if(index !== -1){
        if(cart[index].quantity > 1){
           cart[index].quantity--;
           req.session.total--;
        }
        else{
           cart.splice(index, 1);
           req.session.total--;
        }
     }
  
     return res.sendStatus(204);
})


module.exports = router;