import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Loader2, Mail, Gift, AlertTriangle } from 'lucide-react';
import FoodCarousel from '@/components/FoodCarousel';
import wingstopFood from '@/assets/wingstop-food.jpg';
import pandaFood from '@/assets/panda-food.jpg';
import rubiosFood from '@/assets/rubios-food.jpg';
import blazeFood from '@/assets/blaze-food.jpg';

interface CouponCounts {
  panda: number;
  wingstop: number;
  blaze: number;
  rubios: number;
}

const RestaurantPage = () => {
  const { restaurant } = useParams();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [couponCounts, setCouponCounts] = useState<CouponCounts>({ panda: 0, wingstop: 0, blaze: 0, rubios: 0 });
  const [countsLoading, setCountsLoading] = useState(true);

  const restaurantData = {
    wingstop: {
      name: 'Wingstop',
      discount: 'Free Fries',
      color: 'hsl(var(--wingstop-primary))',
      gradientClass: 'gradient-wingstop',
      buttonVariant: 'wingstop' as const,
      image: wingstopFood,
      foods: [
        { name: 'Regular Seasoned Fries', image: 'https://cdn.bfldr.com/NDQASMJ1/as/r5js3kn8xrjs6p3nkcwfns98/Seasoned_Fries?auto=webp&format=png&width=675' }
      ]
    },
    panda: {
      name: 'Panda Express',
      discount: 'Free Entree',
      color: 'hsl(var(--panda-primary))',
      gradientClass: 'gradient-panda',
      buttonVariant: 'panda' as const,
      image: pandaFood,
      foods: [
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
        { name: 'Super Greens', image: 'https://nomnom-files.pandaexpress.com/global/assets/modifiers/Vegetables_SuperGreens.png', restaurant: 'Panda Express' }
      ]
    },
    rubios: {
      name: "Rubio's",
      discount: 'Free Drink/Dessert',
      color: 'hsl(var(--rubios-primary))',
      gradientClass: 'gradient-rubios',
      buttonVariant: 'rubios' as const,
      image: rubiosFood,
      foods: [
        { name: 'Piña Colada Churro', image: 'https://olo-images-live.imgix.net/22/220f8d2d6d864d71998cc21f8f04cdb8.jpg?auto=format%2Ccompress&q=60&cs=tinysrgb&w=1200&h=800&fit=fill&fm=png32&bg=transparent&s=5fee6f1c7c13f98dfcc851bdbdeb5d49' },
        { name: 'Warm Cinnamon Churro', image: 'https://olo-images-live.imgix.net/36/369690553f9d4b62be441da9dac27700.jpg?auto=format%2Ccompress&q=60&cs=tinysrgb&w=1200&h=800&fit=fill&fm=png32&bg=transparent&s=d25aa56091393e7d26dfb50bfa89f1bb' },
        { name: 'Chocolate Chunk Cookie', image: 'https://i.ytimg.com/vi/tVnLnskzx_Q/oardefault.jpg?sqp=-oaymwEYCJUDENAFSFqQAgHyq4qpAwcIARUAAIhC&rs=AOn4CLDtxkYdFiq-fG_dFy1bg-iedzN6_A' },
        { name: 'Salted Caramel Cookie', image: 'https://olo-images-live.imgix.net/41/4185d145ef6544648db170efce20f783.jpg?auto=format%2Ccompress&q=60&cs=tinysrgb&w=1200&h=800&fit=fill&fm=png32&bg=transparent&s=2f02dcb040cbc7dabbb50fae58c22445' },
        { name: 'Gluten Free Honduran Chocolate Brownie', image: 'https://olo-images-live.imgix.net/4d/4dea61321f1e4cf9a078d716ef220300.jpg?auto=format%2Ccompress&q=60&cs=tinysrgb&w=1200&h=800&fit=fill&fm=png32&bg=transparent&s=0abfc443ad5fd69af6db5db2f2002c33' },
        { name: 'Toffee Crunch Blondie', image: 'https://olo-images-live.imgix.net/07/07f7e59331864c6b88df077c6c20edfa.jpg?auto=format%2Ccompress&q=60&cs=tinysrgb&w=1200&h=800&fit=fill&fm=png32&bg=transparent&s=9830c62cfc5a2f42b225ef74480b8735' },
        { name: 'Large Drink', image: 'https://olo-images-live.imgix.net/68/68737aba8a8b4e08a188130aab014246.jpg?auto=format%2Ccompress&q=60&cs=tinysrgb&w=1200&h=800&fit=fill&fm=png32&bg=transparent&s=93c756240ce72b3137cf543c0bb7180e' },
        { name: 'Bottled Drinks', image: 'https://olo-images-live.imgix.net/5e/5e154b27fcd84ca88e5eb80af572f529.jpg?auto=format%2Ccompress&q=60&cs=tinysrgb&w=1200&h=800&fit=fill&fm=png32&bg=transparent&s=2b1662c9003c1df603a95c9186861aa1' }
      ]
    },
    blaze: {
      name: 'Blaze Pizza',
      discount: 'Free Dessert',
      color: 'hsl(var(--blaze-primary))',
      gradientClass: 'gradient-blaze',
      buttonVariant: 'blaze' as const,
      image: blazeFood,
      foods: [
        { name: 'Cinnamon Bread', image: 'https://olo-images-live.imgix.net/c8/c81fa568bcd1402fb5e9b4b6eb311457.jpg?auto=format%2Ccompress&q=60&cs=tinysrgb&w=2560&h=512&fit=fill&fm=png32&bg=transparent&s=ac660731b99e44f7dae7b1f2f2507545' },
        { name: "S'more Pie", image: 'https://olo-images-live.imgix.net/16/16a9b0e35ecd44049a3934cbc6ce0517.jpg?auto=format%2Ccompress&q=60&cs=tinysrgb&w=2560&h=512&fit=fill&fm=png32&bg=transparent&s=4744cc8bee2c6289a0355a6aed080c74' },
        { name: 'Chocolate Brownie', image: 'https://olo-images-live.imgix.net/09/09546f6d530c40578d4b3747c1cbb562.jpg?auto=format%2Ccompress&q=60&cs=tinysrgb&w=2560&h=512&fit=fill&fm=png32&bg=transparent&s=541531e420b392b1bbdb06ec37a17495' },
        { name: 'Chocolate Chip Cookie', image: 'https://olo-images-live.imgix.net/2b/2b6b18884c994069aa12d92833528bc1.jpg?auto=format%2Ccompress&q=60&cs=tinysrgb&w=2560&h=512&fit=fill&fm=png32&bg=transparent&s=7d21517f2f88fc32da5bd27095d4f231' }
      ]
    }
  };

  const currentRestaurant = restaurant ? restaurantData[restaurant as keyof typeof restaurantData] : null;

  // Fetch coupon counts for lightning mode restaurants
  useEffect(() => {
    const fetchCouponCounts = async () => {
      try {
        const response = await fetch('/api/coupon-counts');
        if (response.ok) {
          const data = await response.json();
          if (data.success) {
            setCouponCounts(data.counts);
          }
        }
      } catch (error) {
        console.error('Error fetching coupon counts:', error);
      } finally {
        setCountsLoading(false);
      }
    };

    fetchCouponCounts();
  }, []);

  if (!currentRestaurant) {
    return (
      <div className="container mx-auto px-4 py-20 text-center">
        <h1 className="text-3xl font-bold mb-4">Restaurant Not Found</h1>
        <Button onClick={() => navigate('/')}>Back to Home</Button>
      </div>
    );
  }

  // Get current restaurant's coupon count
  const getCurrentCouponCount = () => {
    if (restaurant === 'panda') return couponCounts.panda;
    if (restaurant === 'wingstop') return couponCounts.wingstop;
    if (restaurant === 'blaze') return couponCounts.blaze;
    if (restaurant === 'rubios') return couponCounts.rubios;
    return 1; // For other restaurants, always show as available
  };

  const currentCouponCount = getCurrentCouponCount();
  const isCouponsAvailable = currentCouponCount > 0;

  const refreshCouponCounts = async () => {
    try {
      const response = await fetch('/api/coupon-counts');
      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          setCouponCounts(data.counts);
        }
      }
    } catch (error) {
      console.error('Error refreshing coupon counts:', error);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || isLoading || !isCouponsAvailable) return;

    setIsLoading(true);

    try {
      const isLightning = restaurant === 'panda' || restaurant === 'wingstop' || restaurant === 'blaze' || restaurant === 'rubios';
      const endpoint = isLightning 
        ? `/api/restaurants/${restaurant}/lightning`
        : `/api/restaurants/${restaurant}`;

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });

      if (response.ok) {
        const result = await response.json();
        if (result.success) {
          // Refresh coupon counts after successful lightning mode submission
          if (isLightning) {
            await refreshCouponCounts();
          }
          
          // Navigate to result page with URL parameters like original Flask app
          const params = new URLSearchParams({
            code: result.code || '',
            safeexpiredate: result.safeexpiredate || '',
            restaurant: restaurant || '',
            message: result.message || ''
          });
          navigate(`/result?${params.toString()}`);
        } else {
          // Check if API wants us to redirect
          if (result.redirect) {
            navigate(result.redirect);
            return;
          }
          
          // Check for restricted email or invalid email - redirect to error page
          if (result.error && (
            result.error.includes('restricted email') || 
            result.error.includes('Invalid email')
          )) {
            navigate('/error');
            return;
          }
          
          throw new Error(result.error || 'Failed to generate coupon');
        }
      } else {
        const errorData = await response.json().catch(() => ({}));
        
        // Check if API wants us to redirect
        if (errorData.redirect) {
          navigate(errorData.redirect);
          return;
        }
        
        // Check for restricted email or invalid email - redirect to error page
        if (errorData.error && (
          errorData.error.includes('restricted email') || 
          errorData.error.includes('Invalid email')
        )) {
          navigate('/error');
          return;
        }
        
        throw new Error(errorData.error || 'Failed to generate coupon');
      }
    } catch (error) {
      console.error('Error:', error);
      
      // Check if this is a restricted/invalid email error
      const errorMessage = error instanceof Error ? error.message : 'Failed to generate coupon';
      if (errorMessage.includes('restricted email') || errorMessage.includes('Invalid email')) {
        navigate('/error');
        return;
      }
      
      alert(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className={`relative ${currentRestaurant.gradientClass} py-20`}>
        <div className="container mx-auto px-4">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="text-white space-y-6">
              <Badge 
                variant="secondary" 
                className="bg-white/20 text-white border-white/30 backdrop-blur-sm"
              >
                <Gift className="w-4 h-4 mr-2" />
                {currentRestaurant.discount}
              </Badge>
              
              <h1 className="text-5xl font-bold">
                Get Your {currentRestaurant.name} Coupon
              </h1>
              
              <p className="text-xl text-white/90 mb-8">
                {restaurant === 'wingstop' && 'Get a Free Regular Fries with your next online order.'}
                {restaurant === 'panda' && 'Get a Free Small Entrée with purchase of a 2-entrée Plate.'}
                {restaurant === 'rubios' && 'Get a Free Drink or Dessert with your next online order.'}
                {restaurant === 'blaze' && 'Get a Free Dessert with your next online order.'}
                <br />
                <span className="text-lg">Enter your email below - No surveys, no waiting.</span>
              </p>

              {/* Coupons Left Counter - Only for Lightning Mode Restaurants */}
              {(restaurant === 'wingstop' || restaurant === 'panda' || restaurant === 'blaze' || restaurant === 'rubios') && (
                <div className="mb-4 text-center">
                  {countsLoading ? (
                    <div className="inline-flex items-center gap-2 px-4 py-2 bg-white/20 backdrop-blur-md rounded-full border border-white/30">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse"></div>
                      <span className="text-white/90 text-sm font-medium">
                        Loading coupons...
                      </span>
                    </div>
                  ) : (
                    <div className={`inline-flex items-center gap-2 px-4 py-2 backdrop-blur-md rounded-full border ${
                      isCouponsAvailable 
                        ? 'bg-white/20 border-white/30' 
                        : 'bg-red-500/20 border-red-500/30'
                    }`}>
                      {isCouponsAvailable ? (
                        <div className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse"></div>
                      ) : (
                        <AlertTriangle className="w-3 h-3 text-red-400" />
                      )}
                      <span className="text-white/90 text-sm font-medium">
                        <span className={`font-bold ${isCouponsAvailable ? 'text-white' : 'text-red-300'}`}>
                          {currentCouponCount}
                        </span> {currentCouponCount === 1 ? 'coupon' : 'coupons'} {isCouponsAvailable ? 'left' : 'available'}
                      </span>
                    </div>
                  )}
                </div>
              )}

              {/* Email Form */}
              <Card className="p-6 bg-white/10 backdrop-blur-md border-white/20">
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div className="relative">
                    <Mail className="absolute left-3 top-3 w-5 h-5 text-white/70" />
                    <Input
                      type="email"
                      placeholder="Enter your email address"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      className="pl-10 bg-white/20 border-white/30 text-white placeholder:text-white/70 focus:bg-white/30"
                      required
                      disabled={isLoading}
                    />
                  </div>

                  <Button 
                    type="submit" 
                    variant={currentRestaurant.buttonVariant}
                    size="lg"
                    className="w-full"
                    disabled={isLoading || !email || !isCouponsAvailable}
                  >
                    {isLoading ? (
                      <>
                        <Loader2 className="w-4 h-4 animate-spin mr-2" />
                        Generating Coupon...
                      </>
                    ) : !isCouponsAvailable && (restaurant === 'panda' || restaurant === 'wingstop' || restaurant === 'blaze' || restaurant === 'rubios') ? (
                      <>
                        <AlertTriangle className="w-4 h-4 mr-2" />
                        No Coupons Available
                      </>
                    ) : (
                      <>
                        Generate Coupon
                      </>
                    )}
                  </Button>
                </form>

                <div className="mt-4 text-center text-sm text-white/80">
                  {!isCouponsAvailable && (restaurant === 'panda' || restaurant === 'wingstop' || restaurant === 'blaze' || restaurant === 'rubios') ? (
                    <p className="text-red-300">
                      ⚠️ No coupons currently available. Will automaticallyrestock later tonight!
                    </p>
                  ) : (
                    <p>⚡ Instant delivery • 💲 Free • 📧 No spam</p>
                  )}
                </div>
              </Card>
            </div>

            <div className="relative">
              <img 
                src={currentRestaurant.image} 
                alt={`${currentRestaurant.name} food`}
                className="w-full h-96 object-cover rounded-2xl shadow-restaurant"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Food Slider Section */}
      <section className="py-16 bg-muted/30">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <FoodCarousel 
              foods={currentRestaurant.foods} 
              restaurant={currentRestaurant.name}
            />
          </div>
        </div>
      </section>
    </div>
  );
};

export default RestaurantPage;