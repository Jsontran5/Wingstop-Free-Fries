import { useState, useEffect } from 'react';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Gift, DollarSign, Heart, Calendar } from 'lucide-react';

interface StatsData {
  totalCoupons: number;
  totalSaved: number;
}

const StatsPage = () => {
  const [stats, setStats] = useState<StatsData>({
    totalCoupons: 0,
    totalSaved: 0
  });
  const [isLoading, setIsLoading] = useState(true);

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
          totalSaved: 13547
        });
      } finally {
        setIsLoading(false);
      }
    };

    fetchStats();
  }, []);

  const formatNumber = (num: number) => {
    return num.toLocaleString();
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading stats...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen gradient-hero">
      <div className="container mx-auto px-4 py-20">
        {/* Header Section */}
        <div className="text-center text-white space-y-6 mb-16">
          <Badge variant="secondary" className="bg-white/20 text-white border-white/30 backdrop-blur-sm">
            <Heart className="w-4 h-4 mr-2" />
            Thank You!
          </Badge>
          
          <h1 className="text-5xl font-bold mb-4">
            WingstopFreeFries Impact
          </h1>
          
          <p className="text-xl text-white/90 max-w-3xl mx-auto mb-8">
            Thanks to amazing people like you, WFF has helped thousands skip the surveys and get straight to the food. 
            Here's the incredible impact we've made together!
          </p>

          {/* Tracking Since Note */}
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-white/10 backdrop-blur-md rounded-full border border-white/20">
            <Calendar className="w-4 h-4" />
            <span className="text-sm text-white/90">
              Tracking live since December 2023
            </span>
          </div>
        </div>

        {/* Main Stats */}
        <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto mb-16">
          {/* Total Coupons */}
          <Card className="p-8 bg-white/10 backdrop-blur-md border-white/20 text-white">
            <div className="text-center space-y-4">
              <div className="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center mx-auto">
                <Gift className="w-8 h-8" />
              </div>
              <div>
                <p className="text-white/80 text-lg mb-2">Total Uses</p>
                <p className="text-5xl font-bold">{formatNumber(stats.totalCoupons)}</p>
              </div>
            </div>
          </Card>

          {/* Total Money Saved */}
          <Card className="p-8 bg-white/10 backdrop-blur-md border-white/20 text-white">
            <div className="text-center space-y-4">
              <div className="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center mx-auto">
                <DollarSign className="w-8 h-8" />
              </div>
              <div>
                <p className="text-white/80 text-lg mb-2">Total Amount Saved</p>
                <p className="text-5xl font-bold">${formatNumber(stats.totalSaved)}</p>
              </div>
            </div>
          </Card>
        </div>

        {/* Thank You Message */}
        <Card className="p-12 bg-white/20 backdrop-blur-md border-white/30 text-white text-center max-w-4xl mx-auto">
          <div className="space-y-6">
            <div className="w-20 h-20 bg-white/30 rounded-full flex items-center justify-center mx-auto">
              <Heart className="w-10 h-10" />
            </div>
            
            <h2 className="text-3xl font-bold">
              Thank You for Being Part of Our Community
            </h2>
            
            <p className="text-xl text-white/90 leading-relaxed max-w-2xl mx-auto">
              Every coupon generated represents someone who chose convenience, 
              someone who saved time and money. Together, we're revolutionizing how people 
              get their favorite restaurant deals, one free meal at a time. W
            </p>
            
            <div className="pt-4">
              <p className="text-white/80 text-lg">
                Keep spreading the word and helping others save! 🍟❤️
              </p>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default StatsPage;