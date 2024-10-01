
const express = require("express");
const router = express.Router();
const data = require("../data/mydata");

router.get("/", (req, res) => {
    res.redirect("/home/getCategories");
})

router.get("/home/getCategories", (req, res) => {
    
    let cat = [];
    cat = data.categories;

    res.render("home", {
        session: req.session,
        categories: cat,
        category: "Performance",
        products: data.categories.find(category => category.name === "Performance").products 
    })

})

router.get("/home/getProducts/:id", (req, res) => {

    let cat = req.params.id;
    let items = data.categories.find(category => category.name === cat).products;

    res.render("home", {
        session: req.session,
        products: items,
        category: cat,
        categories: data.categories
    })

})


module.exports = router;
