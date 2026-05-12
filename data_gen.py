import pandas as pd
import random

def create_dataset():
    # 1. Product Hierarchy
    data_map = {
        "Refrigerator": {
            "Samsung": ["Bespoke French Door", "Digital Inverter Double Door", "Side-by-Side 700L"],
            "Whirlpool": ["Protton 3-Door", "Intellifresh Pro", "NeoFresh Glass Door"],
            "LG": ["InstaView Door-in-Door", "GL-B201 Single Door", "Linear Inverter Frost Free"],
            "Haier": ["HRB-3404BS", "Bottom Mounted Series", "Glass Door Double Door"],
            "Bosch": ["Serie 4 Freestanding", "Serie 6 Multi-Door", "VarioInverter"]
        },
        "Washing Machine": {
            "Samsung": ["EcoBubble Front Load", "WA65 Top Load", "AI Control Steam"],
            "LG": ["Vivace 8kg", "ThinQ Front Load", "P7001 Top Load"],
            "Bosch": ["Serie 6 Front Load", "Serie 4 WGA", "HomeProfessional"],
            "IFB": ["Senator Neo", "Serena ZXS", "Elite Plus VX"],
            "Haier": ["HW80-IM12929", "Ocean Series", "HWM70-707NZP"]
        },
        "Laptops": {
            "Apple": ["MacBook Air M2", "MacBook Pro M3", "MacBook Air M1"],
            "Dell": ["XPS 13", "Inspiron 15 3000", "Alienware m16"],
            "Lenovo": ["ThinkPad X1 Carbon", "Yoga Slim 7", "Legion 5 Pro"],
            "HP": ["Spectre x360", "Pavilion 15", "Omen Gaming"],
            "Asus": ["ROG Zephyrus G14", "Zenbook 14", "Vivobook S15"]
        },
        "Mobile phones": {
            "Apple": ["iPhone 15 Pro", "iPhone 14", "iPhone 13 Mini"],
            "Samsung": ["Galaxy S24 Ultra", "Galaxy Z Fold 5", "Galaxy A54"],
            "Xiaomi": ["Redmi Note 13 Pro", "Xiaomi 14", "Poco X6 Pro"],
            "OnePlus": ["OnePlus 12", "OnePlus Nord CE 3", "OnePlus 11R"],
            "Motorola": ["Edge 40 Neo", "Razr 40 Ultra", "Moto G84"]
        },
        "Television": {
            "Samsung": ["Neo QLED 8K", "The Frame TV", "Crystal 4K UHD"],
            "LG": ["OLED C3 Series", "QNED 81", "NanoCell 75"],
            "Sony": ["Bravia XR A80L", "X80L 4K HDR", "Bravia XR Master"],
            "TCL": ["C645 QLED", "P635 4K", "Mini LED C845"],
            "Panasonic": ["OLED MZ1500", "VIERA 4K", "Life+ Screen"]
        }
    }
    
    # Updated: Replaced "New-Arrivals" with "On-Site-Visit"
    platforms = ["Amazon", "Flipkart", "Croma", "Reliance Digital", "Vijay Sales", "On-Site-Visit"]
    
    # 2. Diverse Review Library including In-Store Experience
    reviews_library = {
        "POSITIVE": [
            "Excellent performance and build quality.",
            "Great experience at the store, the demo was very helpful.",
            "Loved seeing the product in person before buying. Premium feel!",
            "Store staff was knowledgeable and the product works perfectly.",
            "Best purchase! The on-site visit convinced me to go for this model.",
            "Very sleek design and extremely user-friendly.",
            "The in-store discount was a great bonus. Product is top-notch.",
            "Great value for money, outperforms competitors."
        ],
        "NEUTRAL": [
            "It is an okay product, does what it says.",
            "Visited the store; product is fine but the staff was a bit busy.",
            "Decent quality, but I expected more features after seeing the demo.",
            "Standard performance, similar to the previous year's model.",
            "The on-site visit was helpful but the stock was limited.",
            "Works as intended, but the build could be sturdier.",
            "Satisfactory purchase, but nothing extraordinary.",
            "Middle of the road. It gets the job done."
        ],
        "NEGATIVE": [
            "Poor build quality, stopped working after a week.",
            "In-store demo unit looked much better than what was delivered.",
            "Staff at the store didn't know the specs. Very disappointed.",
            "Not worth the price. Much better options available in other stores.",
            "The on-site visit was a waste of time, product was out of stock.",
            "Defective unit received, and the store is refusing to help.",
            "Battery life is terrible compared to what the salesperson said.",
            "Loud noise during operation, very distracting."
        ]
    }

    final_data = []
    
    # 3. Chronological Generation Logic
    for cat in data_map.keys():
        for brand in data_map[cat].keys():
            for model in data_map[cat][brand]:
                for plat in platforms:
                    # Creating ~22 reviews per combination to hit 10,000 rows
                    for _ in range(23):
                        rand_val = random.random()
                        if rand_val < 0.5:
                            sentiment = "POSITIVE"
                        elif rand_val < 0.8:
                            sentiment = "NEGATIVE"
                        else:
                            sentiment = "NEUTRAL"
                            
                        rev = random.choice(reviews_library[sentiment])
                        final_data.append([cat, brand, model, plat, rev, sentiment])

    df = pd.DataFrame(final_data, columns=["Category", "Brand", "Model", "Platform", "Review", "Ground_Truth"])
    
    # Force exactly 10,000 rows
    df = df.iloc[:10000] 
    
    df.to_csv("reviews_master.csv", index=False)
    print(f"✅ Omnichannel Database Generated: 10,000 rows saved with 'reviews_master' data.")

if __name__ == "__main__":
    create_dataset()