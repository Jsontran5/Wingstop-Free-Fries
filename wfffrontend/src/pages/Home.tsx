import { useState, useEffect } from 'react';
import RestaurantCard from '@/components/RestaurantCard';
import HomeFoodCarousel from '@/components/HomeFoodCarousel';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { TrendingUp, Users, DollarSign, Zap, Gift, User } from 'lucide-react';
import heroImage from '@/assets/hero-image.jpg';
import wingstopFood from '@/assets/wingstop-food.jpg';
import pandaFood from '@/assets/panda-food.jpg';
import rubiosFood from '@/assets/rubios-food.jpg';
import blazeFood from '@/assets/blaze-food.jpg';

interface StatsData {
  totalCoupons: number;
  totalSaved: number;
}

const Home = () => {
  const [stats, setStats] = useState<StatsData>({
    totalCoupons: 0,
    totalSaved: 0
  });
  const [statsLoading, setStatsLoading] = useState(true);

  // Fetch stats data
  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await fetch('/api/stats');
        if (response.ok) {
          const data = await response.json();
          setStats({
            totalCoupons: data.totalCoupons || 0,
            totalSaved: data.totalSaved || 0
          });
        } else {
          throw new Error('Failed to fetch stats');
        }
      } catch (error) {
        console.error('Error fetching stats:', error);
        // Fallback to demo data if API fails
        setStats({
          totalCoupons: 52847,
          totalSaved: 127823
        });
      } finally {
        setStatsLoading(false);
      }
    };

    fetchStats();
  }, []);

  const formatNumber = (num: number) => {
    return num.toLocaleString();
  };

  const restaurants = [
    {
      name: 'Wingstop',
      discount: 'Free Fries',
      image: wingstopFood,
      path: '/restaurant/wingstop',
      gradientClass: 'from-emerald-600 to-emerald-500',
      color: 'hsl(var(--wingstop-primary))'
    },
    {
      name: 'Panda Express',
      discount: 'Free Entree',
      image: pandaFood,
      path: '/restaurant/panda',
      gradientClass: 'from-red-600 to-yellow-500',
      color: 'hsl(var(--panda-primary))'
    },
    {
      name: 'Rubio\'s',
      discount: 'Free Drink/Dessert',
      image: rubiosFood,
      path: '/restaurant/rubios',
      gradientClass: 'from-blue-500 to-orange-500',
      color: 'hsl(var(--rubios-primary))'
    },
    {
      name: 'Blaze Pizza',
      discount: 'Free Dessert',
      image: blazeFood,
      path: '/restaurant/blaze',
      gradientClass: 'from-red-500 to-orange-500',
      color: 'hsl(var(--blaze-primary))'
    }
  ];

  const features = [
    {
      icon: <Zap className="w-6 h-6" />,
      title: 'Instant Coupons',
      description: 'Get your discount codes in seconds!!!'
    },
    {
      icon: <DollarSign className="w-6 h-6" />,
      title: 'Big Savings',
      description: 'Save money on every order at your favorite restaurants'
    },
    {
      icon: <User className="w-6 h-6" />,
      title: 'Solo Developed',
      description: 'Built and maintained by one developer - personal support guaranteed <3'
    }
  ];

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <section className="container mx-auto px-4 py-12">
        <div className="text-center space-y-6">
          <Badge 
            variant="secondary" 
            className="bg-primary/10 text-primary border-primary/20"
          >
            🔥 Coupons On Demand
          </Badge>
          <h1 className="text-4xl lg:text-5xl font-bold leading-tight">
            Skip the Survey,
            <span className="text-gradient block">Get Free Food</span>
          </h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Instantly generate coupons for your favorite restaurants. 
            No more filling out those lengthy surveys.
          </p>
        </div>
      </section>

      {/* Restaurants Section */}
      <section className="container mx-auto px-4">
        <div className="text-center mb-8">
          <h2 className="text-2xl font-bold mb-2">Choose Your Restaurant</h2>
          <p className="text-muted-foreground">
            Get instant coupons for your favorites
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {restaurants.map((restaurant, index) => (
            <RestaurantCard
              key={index}
              {...restaurant}
            />
          ))}
        </div>
      </section>

      {/* Food Carousel */}
      <HomeFoodCarousel />

      {/* Features Section */}
      <section className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold mb-4">Why Use WingstopFreeFries?</h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            I automated the boring stuff so you can focus on enjoying great food at great prices. Who doesn't like free food? 
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <Card key={index} className="p-6 text-center shadow-card border-border/50 bg-card/50 backdrop-blur-sm">
              <div className="w-12 h-12 mx-auto mb-4 rounded-full bg-primary/10 flex items-center justify-center text-primary">
                {feature.icon}
              </div>
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-muted-foreground">{feature.description}</p>
            </Card>
          ))}
        </div>
      </section>

      {/* Stats Preview */}
      <section className="container mx-auto px-4">
        <Card className="p-8 text-center gradient-hero shadow-restaurant">
          <div className="grid md:grid-cols-2 gap-12 text-white max-w-2xl mx-auto">
            <div>
              <Gift className="w-8 h-8 mx-auto mb-2" />
              <div className="text-3xl font-bold">
                {statsLoading ? '...' : formatNumber(stats.totalCoupons)}
              </div>
              <div className="text-white/80">Total Uses</div>
            </div>
            <div>
              <DollarSign className="w-8 h-8 mx-auto mb-2" />
              <div className="text-3xl font-bold">
                ${statsLoading ? '...' : formatNumber(stats.totalSaved)}
              </div>
              <div className="text-white/80">Dollars Saved</div>
            </div>
          </div>
        </Card>
      </section>
    </div>
  );
};

export default Home;