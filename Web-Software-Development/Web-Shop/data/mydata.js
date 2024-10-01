
const data = {
    "website": "Automobili",
    "categories": [
        { 
            "name" : "Sedan",
            "products" : [
                { 
                    "id" : 1, "name" : "Audi A4", "image" : "/images/sedan-audi-a4.jpg"
                },
                { 
                    "id" : 2, "name" : "BMW Serija 5", "image" : "/images/sedan-bmw-5.jpg"
                },                
                { 
                    "id" : 3, "name" : "Mercedes-Benz E Klasa", "image" : "/images/sedan-e-class.jpeg"
                },
                { 
                    "id" : 4, "name" : "Jaguar XF", "image" : "/images/sedan-jaguar-xf.jpeg"
                },
                { 
                    "id" : 5, "name" : "Alfa Romeo Giulia", "image" : "/images/sedan-alfa-giulia.jpg"
                }
            ]
        },
        { 
            "name" : "Coupé",
            "products" : [
                { 
                    "id" : 6, "name" : "Audi A5 Coupe", "image" : "/images/coupe-audi-a5.jpeg"
                },
                { 
                    "id" : 7, "name" : "BMW Serija 4 Coupe", "image" : "/images/coupe-bmw-4.jpg"
                },                
                { 
                    "id" : 8, "name" : "BMW Serija 2 Coupe", "image" : "/images/coupe-bmw-2.jpg"
                },
                { 
                    "id" : 9, "name" : "Mercedes-Benz C Klasa Coupe", "image" : "/images/coupe-c-class.jpg"
                },
                { 
                    "id" : 10, "name" : "Mercedes-Benz E Klasa Coupe", "image" : "/images/coupe-e-class.jpg"
                }
            ]
        },
        { 
            "name" : "SUV",
            "products" : [
                { 
                    "id" : 11, "name" : "Audi Q5", "image" : "/images/suv-q5.jpg"
                },
                { 
                    "id" : 12, "name" : "BMW X5", "image" : "/images/suv-x5.jpg"
                },                
                { 
                    "id" : 13, "name" : "Mercedes-Benz GLC", "image" : "/images/suv-glc.jpg"
                },
                { 
                    "id" : 14, "name" : "Jaguar F-Pace", "image" : "/images/suv-f-pace.jpg"
                },
                { 
                    "id" : 15, "name" : "Range Rover Evoque", "image" : "/images/suv-evoque.jpg"
                }
            ]
        },
        { 
            "name" : "Hatchback",
            "products" : [
                { 
                    "id" : 16, "name" : "Audi A3", "image" : "/images/hatchback-a3.jpg"
                },
                { 
                    "id" : 17, "name" : "Bmw Serija 1", "image" : "/images/hatchback-bmw-1.jpg"
                },                
                { 
                    "id" : 18, "name" : "Merdeces-Benz A Klasa", "image" : "/images/hatchback-a-class.jpg"
                },
                { 
                    "id" : 19, "name" : "Volkswagen Golf 8", "image" : "/images/hatchback-golf-8.jpg"
                },
                { 
                    "id" : 20, "name" : "MINI Cooper SD", "image" : "/images/hatchback-mini.jpg"
                }
            ]
        },
        { 
            "name" : "Performance",
            "products" : [
                { 
                    "id" : 21, "name" : "Audi RS7", "image" : "/images/sports-rs7.jpg"
                },
                { 
                    "id" : 22, "name" : "BMW M4", "image" : "/images/sports-m4.jpg"
                },                
                { 
                    "id" : 23, "name" : "Mercedes-AMG GT Coupe", "image" : "/images/sports-amg-gt.jpg"
                },
                { 
                    "id" : 24, "name" : "Porsche 911 GT3", "image" : "/images/sports-gt3.jpg"
                },
                { 
                    "id" : 25, "name" : "Jaguar F-Type", "image" : "/images/sports-f-type.jpg"
                }
            ]
        },
        { 
            "name" : "Karavan",
            "products" : [
                { 
                    "id" : 26, "name" : "Audi A6 Avant", "image" : "/images/karavan-a6.jpg"
                },
                { 
                    "id" : 27, "name" : "Audi A4 Allroad", "image" : "/images/karavan-a4.jpg"
                },                
                { 
                    "id" : 28, "name" : "BMW Serija 5 Touring", "image" : "/images/karavan-bmw-5.jpg"
                },
                { 
                    "id" : 29, "name" : "Mercedes-Benz E Klasa Karavan", "image" : "/images/karavan-e-class.jpg"
                },
                { 
                    "id" : 30, "name" : "Volvo V90 Cross Country", "image" : "/images/karavan-v90.jpg"
                }
            ]
        },
        { 
            "name" : "Kabriolet",
            "products" : [
                { 
                    "id" : 31, "name" : "Audi A5 Kabriolet", "image" : "/images/kabrio-a5.jpg"
                },
                { 
                    "id" : 32, "name" : "BMW Serija 4 Kabriolet", "image" : "/images/kabrio-bmw-4.jpg"
                },                
                { 
                    "id" : 33, "name" : "Mercedes-Benz SL", "image" : "/images/kabrio-sl.jpg"
                },
                { 
                    "id" : 34, "name" : "Porsche 911 Carrera Kabriolet", "image" : "/images/kabrio-carrera.jpg"
                },
                { 
                    "id" : 35, "name" : "Porsche 718 Boxster", "image" : "/images/kabrio-boxster.jpg"
                }
            ]
        },
        { 
            "name" : "Limuzina",
            "products" : [
                { 
                    "id" : 36, "name" : "Audi A8", "image" : "/images/limuzina-a8.jpeg"
                },
                { 
                    "id" : 37,  "name" : "BMW Serija 7", "image" : "/images/limuzina-bmw-7.jpg"
                },                
                { 
                    "id" : 38, "name" : "Mercedes-Benz S Klasa", "image" : "/images/limuzina-s-class.jpg"
                },
                { 
                    "id" : 39, "name" : "Jaguar XE", "image" : "/images/limuzina-xe.jpg"
                },
                { 
                    "id" : 40, "name" : "Lexus LS", "image" : "/images/limuzina-lexus-ls.jpg"
                }
            ]
        },
        { 
            "name" : "Električni",
            "products" : [
                { 
                    "id" : 41, "name" : "Mercedes-Benz EQE", "image" : "/images/electric-eqe.jpg"
                },
                { 
                    "id" : 42, "name" : "BMW i4", "image" : "/images/electric-bmw-i4.jpg"
                },                
                { 
                    "id" : 43, "name" : "Tesla Model 3", "image" : "/images/electric-tesla.jpg"
                },
                { 
                    "id" : 44, "name" : "Porsche Taycan", "image" : "/images/electric-taycan.jpg"
                },
                { 
                    "id" : 45, "name" : "Volkswagen ID.7", "image" : "/images/electric-id7.jpg"
                }
            ]
        },
        { 
            "name" : "Special",
            "products" : [
                { 
                    "id" : 46, "name" : "Aston Martin DBS Superleggera", "image" : "/images/special-dbs.jpg"
                },
                { 
                    "id" : 47, "name" : "Bentley Continental GT", "image" : "/images/special-bentley.jpg"
                },                
                { 
                    "id" : 48, "name" : "Mercedes-AMG G63", "image" : "/images/special-g63.jpg"
                },
                { 
                    "id" : 49, "name" : "Ferrari 296 GTB", "image" : "/images/special-ferrari.jpg"
                },
                { 
                    "id" : 50, "name" : "Lamborghini Huracan", "image" : "/images/special-huracan.jpg"
                }
            ]
        }


    ]
}

module.exports = data;