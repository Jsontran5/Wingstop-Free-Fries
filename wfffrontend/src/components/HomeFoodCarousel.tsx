import { Card, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import {
  Carousel,
  CarouselContent,
  CarouselItem,
} from './ui/carousel';
import Autoplay from 'embla-carousel-autoplay';
import wingstopFood from '@/assets/wingstop-food.jpg';
import pandaFood from '@/assets/panda-food.jpg';
import rubiosFood from '@/assets/rubios-food.jpg';
import blazeFood from '@/assets/blaze-food.jpg';

interface FoodItem {
  name: string;
  image: string;
  restaurant: string;
}

const HomeFoodCarousel = () => {
  const allFoods: FoodItem[] = [
    // Wingstop
    { name: 'Regular Seasoned Fries', image: 'https://cdn.bfldr.com/NDQASMJ1/as/r5js3kn8xrjs6p3nkcwfns98/Seasoned_Fries?auto=webp&format=png&width=675', restaurant: 'Wingstop' },
    
    // Panda Express
    { name: 'The Original Orange Chicken', image: 'https://nomnom-files.pandaexpress.com/global/assets/modifiers/Chicken_OrangeChicken.png', restaurant: 'Panda Express' },
  { name: 'Black Pepper Sirloin Steak', image: 'https://nomnom-files.pandaexpress.com/global/assets/modifiers/Beef_ShanghaiAngusSteak.png', restaurant: 'Panda Express' },
  { name: 'Honey Walnut Shrimp', image: 'https://nomnom-files.pandaexpress.com/global/assets/modifiers/Seafood_HoneyWalnutShrimp.png', restaurant: 'Panda Express' },
  { name: 'Chicken Egg Roll (1)', image: 'https://olo-images-live.imgix.net/52/524bbb9023e2409b8d3fceae944a808f.png?auto=format%2Ccompress&q=60&cs=tinysrgb&w=810&h=540&fit=crop&fm=png32&s=4f4cc30df356786bbe3968181f8c5160', restaurant: 'Panda Express' },
  { name: 'Veggie Spring Roll (2)', image: 'https://olo-images-live.imgix.net/18/183834b8a35a4737a73a28421f68b4f0.png?auto=format%2Ccompress&q=60&cs=tinysrgb&w=810&h=540&fit=crop&fm=png32&s=0d4be7c417ec1998251da41d5bfe13fb', restaurant: 'Panda Express' },
  { name: 'Cream Cheese Rangoon (3)', image: 'https://olo-images-live.imgix.net/fe/fef7db209d7d41e6ae065af16afa1577.png?auto=format%2Ccompress&q=60&cs=tinysrgb&w=810&h=540&fit=crop&fm=png32&s=f14d518edf4e7ee0fd22b4d3cddc59b8', restaurant: 'Panda Express' },
  { name: 'Apple Pie Roll (1)', image: 'https://olo-images-live.imgix.net/ab/ab4e688dea2b4b56b79fa2ff42a31f24.png?auto=format%2Ccompress&q=60&cs=tinysrgb&w=810&h=540&fit=crop&fm=png32&s=4b9d93576ba69591523a4c60034d54d3', restaurant: 'Panda Express' },
  { name: 'Grilled Teriyaki Chicken', image: 'https://nomnom-files.pandaexpress.com/global/assets/modifiers/Chicken_GrilledTeriyakiChicken.png', restaurant: 'Panda Express' },
  { name: 'Broccoli Beef', image: 'https://nomnom-files.pandaexpress.com/global/assets/modifiers/Beef_BroccoliBeef.png', restaurant: 'Panda Express' },
  { name: 'Kung Pao Chicken', image: 'https://nomnom-files.pandaexpress.com/global/assets/modifiers/Chicken_KungPaoChicken.png', restaurant: 'Panda Express' },
  { name: 'Honey Sesame Chicken Breast', image: 'https://nomnom-files.pandaexpress.com/global/assets/modifiers/ChickenBreast_HoneySesameChickenBreast.png', restaurant: 'Panda Express' },
  { name: 'Beijing Beef', image: 'https://nomnom-files.pandaexpress.com/global/assets/modifiers/Beef_BeijingBeef.png', restaurant: 'Panda Express' },
  { name: 'Mushroom Chicken', image: 'https://nomnom-files.pandaexpress.com/global/assets/modifiers/Chicken_MushroomChicken.png', restaurant: 'Panda Express' },
  { name: 'String Bean Chicken Breast', image: 'https://nomnom-files.pandaexpress.com/global/assets/modifiers/ChickenBreast_StringBeanChickenBreast.png', restaurant: 'Panda Express' },
  { name: 'Black Pepper Chicken', image: 'https://nomnom-files.pandaexpress.com/global/assets/modifiers/Chicken_BlackPepperChicken.png', restaurant: 'Panda Express' },
  { name: 'Super Greens', image: 'https://nomnom-files.pandaexpress.com/global/assets/modifiers/Vegetables_SuperGreens.png', restaurant: 'Panda Express' },
    
    // Rubio's
    { name: 'Piña Colada Churro', image: 'https://olo-images-live.imgix.net/22/220f8d2d6d864d71998cc21f8f04cdb8.jpg?auto=format%2Ccompress&q=60&cs=tinysrgb&w=1200&h=800&fit=fill&fm=png32&bg=transparent&s=5fee6f1c7c13f98dfcc851bdbdeb5d49', restaurant: "Rubio's" },
    { name: 'Chocolate Chunk Cookie', image: 'https://i.ytimg.com/vi/tVnLnskzx_Q/oardefault.jpg?sqp=-oaymwEYCJUDENAFSFqQAgHyq4qpAwcIARUAAIhC&rs=AOn4CLDtxkYdFiq-fG_dFy1bg-iedzN6_A', restaurant: "Rubio's" },
    { name: 'Warm Cinnamon Churro', image: 'https://olo-images-live.imgix.net/36/369690553f9d4b62be441da9dac27700.jpg?auto=format%2Ccompress&q=60&cs=tinysrgb&w=1200&h=800&fit=fill&fm=png32&bg=transparent&s=d25aa56091393e7d26dfb50bfa89f1bb', restaurant: "Rubio's" },
  { name: 'Salted Caramel Cookie', image: 'https://olo-images-live.imgix.net/41/4185d145ef6544648db170efce20f783.jpg?auto=format%2Ccompress&q=60&cs=tinysrgb&w=1200&h=800&fit=fill&fm=png32&bg=transparent&s=2f02dcb040cbc7dabbb50fae58c22445', restaurant: "Rubio's" },
  { name: 'Gluten Free Honduran Chocolate Brownie', image: 'https://olo-images-live.imgix.net/4d/4dea61321f1e4cf9a078d716ef220300.jpg?auto=format%2Ccompress&q=60&cs=tinysrgb&w=1200&h=800&fit=fill&fm=png32&bg=transparent&s=0abfc443ad5fd69af6db5db2f2002c33', restaurant: "Rubio's" },
  { name: 'Toffee Crunch Blondie', image: 'https://olo-images-live.imgix.net/07/07f7e59331864c6b88df077c6c20edfa.jpg?auto=format%2Ccompress&q=60&cs=tinysrgb&w=1200&h=800&fit=fill&fm=png32&bg=transparent&s=9830c62cfc5a2f42b225ef74480b8735', restaurant: "Rubio's" },
  { name: 'Large Drink', image: 'https://olo-images-live.imgix.net/68/68737aba8a8b4e08a188130aab014246.jpg?auto=format%2Ccompress&q=60&cs=tinysrgb&w=1200&h=800&fit=fill&fm=png32&bg=transparent&s=93c756240ce72b3137cf543c0bb7180e', restaurant: "Rubio's" },
  { name: 'Bottled Drinks', image: 'https://olo-images-live.imgix.net/5e/5e154b27fcd84ca88e5eb80af572f529.jpg?auto=format%2Ccompress&q=60&cs=tinysrgb&w=1200&h=800&fit=fill&fm=png32&bg=transparent&s=2b1662c9003c1df603a95c9186861aa1', restaurant: "Rubio's" },
    
    // Blaze Pizza
    { name: 'Cinnamon Bread', image: 'https://olo-images-live.imgix.net/c8/c81fa568bcd1402fb5e9b4b6eb311457.jpg?auto=format%2Ccompress&q=60&cs=tinysrgb&w=2560&h=512&fit=fill&fm=png32&bg=transparent&s=ac660731b99e44f7dae7b1f2f2507545', restaurant: 'Blaze Pizza' },
{ name: "S'more Pie", image: 'https://olo-images-live.imgix.net/16/16a9b0e35ecd44049a3934cbc6ce0517.jpg?auto=format%2Ccompress&q=60&cs=tinysrgb&w=2560&h=512&fit=fill&fm=png32&bg=transparent&s=4744cc8bee2c6289a0355a6aed080c74', restaurant: 'Blaze Pizza' },
{ name: 'Chocolate Brownie', image: 'https://olo-images-live.imgix.net/09/09546f6d530c40578d4b3747c1cbb562.jpg?auto=format%2Ccompress&q=60&cs=tinysrgb&w=2560&h=512&fit=fill&fm=png32&bg=transparent&s=541531e420b392b1bbdb06ec37a17495', restaurant: 'Blaze Pizza' },
{ name: 'Chocolate Chip Cookie', image: 'https://olo-images-live.imgix.net/2b/2b6b18884c994069aa12d92833528bc1.jpg?auto=format%2Ccompress&q=60&cs=tinysrgb&w=2560&h=512&fit=fill&fm=png32&bg=transparent&s=7d21517f2f88fc32da5bd27095d4f231', restaurant: 'Blaze Pizza' },

  ];

  return (
    <section className="py-16 bg-muted/30">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold mb-4">What You Can Get for FREE</h2>

        </div>
        
        <Carousel
          plugins={[
            Autoplay({
              delay: 2000,
              stopOnInteraction: false,
            }),
          ]}
          opts={{
            align: "start",
            loop: true,
          }}
          className="w-full"
        >
          <CarouselContent className="-ml-2 md:-ml-4">
            {allFoods.map((food, index) => (
              <CarouselItem key={index} className="pl-2 md:pl-4 basis-full sm:basis-1/2 md:basis-1/3 lg:basis-1/4 xl:basis-1/5">
                <Card className="overflow-hidden hover-scale h-56">
                  <CardContent className="p-0 relative h-full">
                    <img 
                      src={food.image} 
                      alt={food.name}
                      className="w-full h-full object-cover"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent" />
                    
                    {/* Restaurant Badge */}
                    <Badge 
                      variant="secondary" 
                      className="absolute top-3 left-3 bg-black/50 text-white border-0 text-xs backdrop-blur-sm"
                    >
                      {food.restaurant}
                    </Badge>
                    
                    {/* FREE Badge */}
                    <Badge 
                      variant="secondary" 
                      className="absolute top-3 right-3 bg-green-500 text-white border-0 font-bold"
                    >
                      FREE
                    </Badge>
                    
                    <div className="absolute bottom-3 left-3 right-3 space-y-1">
                      <h4 className="text-white font-semibold text-sm leading-tight">{food.name}</h4>
                    </div>
                  </CardContent>
                </Card>
              </CarouselItem>
            ))}
          </CarouselContent>
        </Carousel>
        
        <div className="text-center mt-8">
          <p className="text-sm text-muted-foreground">
            Hungry?
          </p>
        </div>
      </div>
    </section>
  );
};

export default HomeFoodCarousel;