// Dummy data for prototype - 20 items following the schema
export const dummyItems = [
  {
    id: "rolex-submariner",
    name: "Rolex Submariner",
    category: "luxury",
    price: 8500,
    img_url: "/img/rolex-submariner.jpg",
    spouse_variant_price: 8500,
    kid_variant_price: null
  },
  {
    id: "birkin-bag",
    name: "Hermès Birkin Bag",
    category: "luxury",
    price: 12000,
    img_url: "/img/birkin-bag.jpg",
    spouse_variant_price: 12000,
    kid_variant_price: null
  },
  {
    id: "tesla-model-s",
    name: "Tesla Model S",
    category: "transport",
    price: 90000,
    img_url: "/img/tesla-s.jpg",
    spouse_variant_price: 70000,
    kid_variant_price: null
  },
  {
    id: "manhattan-apartment",
    name: "Manhattan 2BR Apartment",
    category: "housing",
    price: 60000,
    img_url: "/img/manhattan-apt.jpg",
    spouse_variant_price: null,
    kid_variant_price: 24000
  },
  {
    id: "private-school-tuition",
    name: "Private School Tuition",
    category: "education",
    price: 35000,
    img_url: "/img/private-school.jpg",
    spouse_variant_price: null,
    kid_variant_price: 35000
  },
  {
    id: "nanny-fulltime",
    name: "Full-time Nanny",
    category: "services",
    price: 60000,
    img_url: "/img/nanny.jpg",
    spouse_variant_price: null,
    kid_variant_price: 60000
  },
  {
    id: "engagement-ring",
    name: "Tiffany Engagement Ring",
    category: "life-events",
    price: 15000,
    img_url: "/img/engagement-ring.jpg",
    spouse_variant_price: null,
    kid_variant_price: null
  },
  {
    id: "wedding-ceremony",
    name: "Wedding Ceremony & Reception",
    category: "life-events",
    price: 25000,
    img_url: "/img/wedding.jpg",
    spouse_variant_price: null,
    kid_variant_price: null
  },
  {
    id: "personal-trainer",
    name: "Personal Trainer 3x/week",
    category: "services",
    price: 15000,
    img_url: "/img/trainer.jpg",
    spouse_variant_price: 15000,
    kid_variant_price: null
  },
  {
    id: "michelin-dining",
    name: "Monthly Michelin Dining",
    category: "dining",
    price: 6000,
    img_url: "/img/michelin.jpg",
    spouse_variant_price: 6000,
    kid_variant_price: null
  },
  {
    id: "european-vacation",
    name: "3-Week European Tour",
    category: "travel",
    price: 25000,
    img_url: "/img/europe.jpg",
    spouse_variant_price: 15000,
    kid_variant_price: 10000
  },
  {
    id: "designer-wardrobe",
    name: "Seasonal Designer Updates",
    category: "fashion",
    price: 20000,
    img_url: "/img/wardrobe.jpg",
    spouse_variant_price: 20000,
    kid_variant_price: null
  },
  {
    id: "country-club-membership",
    name: "Country Club Membership",
    category: "luxury",
    price: 25000,
    img_url: "/img/country-club.jpg",
    spouse_variant_price: 15000,
    kid_variant_price: null
  },
  {
    id: "wine-collection",
    name: "Wine Collection Starter",
    category: "luxury",
    price: 10000,
    img_url: "/img/wine-collection.jpg",
    spouse_variant_price: null,
    kid_variant_price: null
  },
  {
    id: "gym-equinox",
    name: "Equinox Membership",
    category: "health",
    price: 3600,
    img_url: "/img/equinox.jpg",
    spouse_variant_price: 3600,
    kid_variant_price: null
  },
  {
    id: "iphone-pro-max",
    name: "iPhone Pro Max Annual",
    category: "tech",
    price: 1500,
    img_url: "/img/iphone.jpg",
    spouse_variant_price: 1500,
    kid_variant_price: null
  },
  {
    id: "golf-clubs-premium",
    name: "Premium Golf Club Set",
    category: "hobbies",
    price: 5000,
    img_url: "/img/golf-clubs.jpg",
    spouse_variant_price: 5000,
    kid_variant_price: null
  },
  {
    id: "theater-season-tickets",
    name: "Broadway Season Tickets",
    category: "entertainment",
    price: 5000,
    img_url: "/img/broadway.jpg",
    spouse_variant_price: 5000,
    kid_variant_price: null
  },
  {
    id: "charity-gala-tables",
    name: "Charity Gala Tables",
    category: "philanthropy",
    price: 20000,
    img_url: "/img/gala.jpg",
    spouse_variant_price: null,
    kid_variant_price: null
  },
  {
    id: "purebred-dog",
    name: "Purebred Puppy",
    category: "pets",
    price: 3000,
    img_url: "/img/puppy.jpg",
    spouse_variant_price: null,
    kid_variant_price: null
  }
];

export const categories = [
  "all",
  "luxury",
  "transport",
  "housing",
  "services",
  "education",
  "life-events",
  "health",
  "dining",
  "fashion",
  "travel",
  "tech",
  "hobbies",
  "entertainment",
  "philanthropy",
  "pets",
  "finance"
];

export const forcedAdds = {
  married: [
    { id: "engagement-ring", quantity: 1 },
    { id: "wedding-ceremony", quantity: 1 }
  ],
  kids: {
    per_child: [
      { id: "private-school-tuition", quantity: 1 }
    ]
  }
};