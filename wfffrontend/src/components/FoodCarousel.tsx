import { Card, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from './ui/carousel';
import { useEffect } from 'react';
import Autoplay from 'embla-carousel-autoplay';

interface FoodItem {
  name: string;
  image: string;
}

interface FoodCarouselProps {
  foods: FoodItem[];
  restaurant: string;
}

const FoodCarousel = ({ foods, restaurant }: FoodCarouselProps) => {
  if (foods.length === 0) return null;

  // Determine if we need carousel functionality (4+ items)
  const needsCarousel = foods.length >= 4;

  return (
    <div className="w-full">
      <h3 className="text-2xl font-semibold mb-6 text-center">
        Coupon Eligible Items
      </h3>
      
      {needsCarousel ? (
        <Carousel
          plugins={[
            Autoplay({
              delay: 3000,
            }),
          ]}
          opts={{
            align: "start",
            loop: true,
          }}
          className="w-full"
        >
          <CarouselContent className="-ml-2 md:-ml-4">
            {foods.map((food, index) => (
              <CarouselItem key={index} className="pl-2 md:pl-4 basis-full sm:basis-1/2 md:basis-1/3 lg:basis-1/4">
                <Card className="overflow-hidden hover-scale h-48">
                  <CardContent className="p-0 relative h-full">
                    <img 
                      src={food.image} 
                      alt={food.name}
                      className="w-full h-full object-cover"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
                    <Badge 
                      variant="secondary" 
                      className="absolute top-3 right-3 bg-green-500 text-white border-0 font-bold"
                    >
                      FREE
                    </Badge>
                    <div className="absolute bottom-3 left-3 right-3">
                      <h4 className="text-white font-semibold text-sm leading-tight">{food.name}</h4>
                    </div>
                  </CardContent>
                </Card>
              </CarouselItem>
            ))}
          </CarouselContent>
          <CarouselPrevious className="left-4" />
          <CarouselNext className="right-4" />
        </Carousel>
      ) : (
        <div className="flex justify-center">
          <div className="w-64">
            {foods.map((food, index) => (
              <Card key={index} className="overflow-hidden hover-scale h-48">
                <CardContent className="p-0 relative h-full">
                  <img 
                    src={food.image} 
                    alt={food.name}
                    className="w-full h-full object-cover"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
                  <Badge 
                    variant="secondary" 
                    className="absolute top-3 right-3 bg-green-500 text-white border-0 font-bold"
                  >
                    FREE
                  </Badge>
                  <div className="absolute bottom-3 left-3 right-3">
                    <h4 className="text-white font-semibold text-sm leading-tight">{food.name}</h4>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default FoodCarousel;