import { Link } from 'react-router-dom';
import { Card } from './ui/card';
import { Badge } from './ui/badge';
import { ArrowRight } from 'lucide-react';

interface RestaurantCardProps {
  name: string;
  discount: string;
  image: string;
  path: string;
  gradientClass: string;
  color: string;
}

const RestaurantCard = ({ 
  name, 
  discount, 
  image, 
  path, 
  gradientClass,
  color 
}: RestaurantCardProps) => {
  return (
    <Link to={path} className="group block">
      <Card className="overflow-hidden transition-smooth hover:scale-105 hover:shadow-restaurant border-border/50 bg-card/50 backdrop-blur-sm">
        <div className={`h-48 bg-gradient-to-br ${gradientClass} relative overflow-hidden`}>
          <img 
            src={image} 
            alt={`${name} food`}
            className="w-full h-full object-cover mix-blend-overlay opacity-60 group-hover:opacity-80 transition-smooth"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
          <div className="absolute top-4 right-4">
            <Badge 
              variant="secondary" 
              className="bg-white/20 text-white border-white/30 backdrop-blur-sm"
            >
              {discount}
            </Badge>
          </div>
        </div>
        
        <div className="p-6">
          <div className="flex items-center justify-between">
            <h3 className="text-xl font-bold mb-2" style={{ color }}>
              {name}
            </h3>
            <ArrowRight className="w-5 h-5 text-muted-foreground group-hover:text-primary transition-smooth group-hover:translate-x-1" />
          </div>
          <p className="text-muted-foreground">
            Get your coupon instantly
          </p>
        </div>
      </Card>
    </Link>
  );
};

export default RestaurantCard;