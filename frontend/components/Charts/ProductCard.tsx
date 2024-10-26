import Link from "next/link";
import Image from "next/image";
import { Product } from "../types/product";

const productData: Product[] = [
  {
    image: "/images/user/user-06.png",
    name: "Organic Green Tea",
    type: "Beverage",
    quantity: 150,
  },
  {
    image: "/images/user/user-06.png",
    name: "Artisan Whole Wheat Bread",
    type: "Bakery",
    quantity: 80,
  },
  {
    image: "/images/user/user-06.png",
    name: "Handmade Ceramic Mug",
    type: "Kitchenware",
    quantity: 40,
  },
  {
    image: "/images/user/user-06.png",
    name: "Eco-friendly Bamboo Toothbrush",
    type: "Personal Care",
    quantity: 200,
  },
  {
    image: "/images/user/user-06.png",
    name: "Organic Almond Butter",
    type: "Groceries",
    quantity: 60,
  },
];

const ProductCard = () => {
  return (
    <div className="col-span-12 rounded-[10px] bg-white py-6 shadow-1 dark:bg-gray-dark dark:shadow-card xl:col-span-4">
      <h4 className="mb-5.5 px-7.5 text-body-2xlg font-bold text-dark dark:text-white">
        Chats
      </h4>

      <div>
        {productData.map((product, key) => (
          <Link
            href="/"
            className="flex items-center gap-4.5 px-7.5 py-3 hover:bg-gray-1 dark:hover:bg-dark-2"
            key={key}
          >
            <div className="relative h-14 w-14 rounded-full">
              <Image
                width={56}
                height={56}
                src={product.image}
                alt="User"
                style={{
                  width: "auto",
                  height: "auto",
                }}
              />
            </div>

            <div className="flex flex-1 items-center justify-between">
              <div>
                <h5 className="font-medium text-dark dark:text-white">
                  {product.name}
                </h5>
                <p>
                  <span className="mb-px text-body-sm font-medium text-dark-3">
                    {product.type}
                  </span>
                  <span className="text-xs">
                    {" "}
                    . Quantity : {product.quantity}
                  </span>
                </p>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default ProductCard;
