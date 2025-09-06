import { useState, useEffect } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { Button } from './ui/button';

interface FoodItem {
  name: string;
  image: string;
}

interface FoodSliderProps {
  foods: FoodItem[];
  restaurant: string;
}

const FoodSlider = ({ foods, restaurant }: FoodSliderProps) => {
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % foods.length);
    }, 3000);

    return () => clearInterval(timer);
  }, [foods.length]);

  const nextSlide = () => {
    setCurrentIndex((prev) => (prev + 1) % foods.length);
  };

  const prevSlide = () => {
    setCurrentIndex((prev) => (prev - 1 + foods.length) % foods.length);
  };

  if (foods.length === 0) return null;

  return (
    <div className="relative">
      <h3 className="text-lg font-semibold mb-4 text-center">
        Popular {restaurant} Items
      </h3>
      
      <div className="relative h-40 rounded-lg overflow-hidden bg-muted">
        <div 
          className="flex transition-transform duration-500 ease-in-out h-full"
          style={{ transform: `translateX(-${currentIndex * 100}%)` }}
        >
          {foods.map((food, index) => (
            <div key={index} className="min-w-full h-full relative">
              <img 
                src={food.image} 
                alt={food.name}
                className="w-full h-full object-cover"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
              <div className="absolute bottom-4 left-4">
                <h4 className="text-white font-semibold">{food.name}</h4>
              </div>
            </div>
          ))}
        </div>

        <Button
          variant="secondary"
          size="icon"
          className="absolute left-2 top-1/2 -translate-y-1/2 bg-white/20 backdrop-blur-sm border-white/30 hover:bg-white/30"
          onClick={prevSlide}
        >
          <ChevronLeft className="w-4 h-4" />
        </Button>

        <Button
          variant="secondary"
          size="icon"
          className="absolute right-2 top-1/2 -translate-y-1/2 bg-white/20 backdrop-blur-sm border-white/30 hover:bg-white/30"
          onClick={nextSlide}
        >
          <ChevronRight className="w-4 h-4" />
        </Button>
      </div>

      <div className="flex justify-center mt-4 space-x-2">
        {foods.map((_, index) => (
          <button
            key={index}
            className={`w-2 h-2 rounded-full transition-smooth ${
              index === currentIndex ? 'bg-primary' : 'bg-muted-foreground/30'
            }`}
            onClick={() => setCurrentIndex(index)}
          />
        ))}
      </div>
    </div>
  );
};

export default FoodSlider;