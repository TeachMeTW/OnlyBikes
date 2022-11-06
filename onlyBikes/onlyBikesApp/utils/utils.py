from ..models import BikeModel

test_bikes = [{
    "user" : "Sally May", 
    "brand" : "Co-op Cycles",
    "model" : "CTY 1.1",
    "price" : 20,
    "condition" : "New",
    "location" : "San Fransisco, CA",
    "image" : "https://i.ebayimg.com/images/g/hnsAAOSwalxhLRn6/s-l500.jpg",
    "description" : "Made for urban cruising. This bike features a low crossbar for easy mounts and dismounts, a flat handlebar for a heads-up ride and a versatile 3x8 drivetrain.",
},{
    "user" : "Robin Shultz",
    "brand" : "Schwinn",
    "model" : "Coston DX",
    "price" : 35,
    "condition" : "Used",
    "location" : "Santa Clara, CA",
    "image" : "https://cloudfront-us-east-1.images.arcpublishing.com/octane/6S2OXJZGXRCWXOZC4RALKFJFQU.jpg",
    "description" : "Schwinn is a brilliant choice as it features both pedal assist and throttle options. We also like that it has integrated lights (helpful when you’re biking home in the dark) and fenders (great for keeping mud off your work clothes on rainy days",
},{
    "user" : "Matthew Jew",
    "brand" : "Cervelo",
    "model" : "Caledonia Ultegra",
    "price" : 25,
    "condition" : "Like New",
    "location" : "New York, NY",
    "image" : "https://cyclingtips.com/wp-content/uploads/2021/01/2021-Cervelo-Caledonia-Ultegra-Di2-road-bike-review-cyclingtips-Field-test-4.jpg",
    "description" : "When you’re ready to move beyond casual rides and start training for distance and speed on pavement, a road bike will be the best fit.",
}, {
    "user" : "Shizuka Nigiyaka",
    "brand" : "VanMoof",
    "model" : "S3",
    "price" : 28,
    "condition" : "Used",
    "location" : "Compton, CA",
    "image" : "https://cdn.pocket-lint.com/r/s/970x/assets/images/152686-fitness-trackers-review-s3-vanmoof-2nd-set-image1-hden5uz0i9.jpg",
    "description" : "VanMoof has fostered something of a following amongst gear heads, and that approval is quickly extending to casual riders too. Sleek and stylish, the S3 e-bike boasts four speed settings, making hills nearly as easy as straightaways.",
},{
    "user" : "Lovemore Dumi",
    "brand" : "Ibis",
    "model" : "Hakka MX Disc 650b",
    "price" : 19,
    "condition" : "New",
    "location" : "Pasadena, CA",
    "image" : "https://www.cxmagazine.com/wp-content/uploads/2018/09/ibis-hakka-mx-cyclocross-gravel-IMG_8448-HDR-cxmagazine-ay_1.jpg",
    "description" : "VanMoof has fostered something of a following amongst gear heads, and that approval is quickly extending to casual riders too. Sleek and stylish, the S3 e-bike boasts four speed settings, making hills nearly as easy as straightaways.",
},{
    "user" : "Efe Aamina",
    "brand" : "Liv",
    "model" : "Alight 2 Disc",
    "price" : 21,
    "condition" : "New",
    "location" : "Condard, CA",
    "image" : "https://s3.amazonaws.com/www.bikerumor.com/wp-content/uploads/2021/11/23191628/showcase7.jpg",
    "description" : "It comes equipped with reliable Shimano components and accessory mounts so you can add fenders, racks or a kickstand depending on whether you use your bike for grocery runs or commuting during the rainy season.",
},{
    "user" : "Oni Ochieng",
    "brand" : "Lectric",
    "model" : "XP Step-Thru 2.0",
    "price" : 25,
    "condition" : "Used",
    "location" : "Condard, CA",
    "image" : "https://cleantechnica.com/files/2021/05/2021.05-lectric-xp-step-thru-cargo-baskets-accessories-ebike-electric-bicycle-KYLE3.jpg",
    "description" : "With high-quality brakes and pedal assist, the XP Step-Thru 2.0 is ideal for commuting and everyday riding. While some folding bikes feel unstable because of their small tires, the long wheel base of this model adds stability and finesse to your ride.",
},
]

def test_data():
    bike_list = []
    for bike_obj in test_bikes:
        bike = BikeModel(
            brand = bike_obj["brand"], 
            model = bike_obj["model"], 
            price = bike_obj["price"], 
            condition = bike_obj["condition"], 
            location = bike_obj["location"], 
            description = bike_obj["description"],
            image_url = bike_obj["image"],
            original_owner = bike_obj["user"]
            )
        # bike.save()
        bike_list.append(bike)

    return bike_list