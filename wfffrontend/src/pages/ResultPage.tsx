import { useLocation, useNavigate, useSearchParams } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Textarea } from '@/components/ui/textarea';
import { CheckCircle, Copy, Home, RotateCcw, Send } from 'lucide-react';
import { useState } from 'react';
import { useToast } from '@/hooks/use-toast';
import pandaLogo from '@/assets/panda-logo.png';
import wingstopBanner from '@/assets/wingstop-banner.png';

const ResultPage = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [copied, setCopied] = useState(false);
  const [feedback, setFeedback] = useState('');
  const [sendingFeedback, setSendingFeedback] = useState(false);
  const [feedbackSent, setFeedbackSent] = useState(false);
  const { toast } = useToast();
  
  // Extract data from URL parameters like original Flask app
  const code = searchParams.get('code');
  const safeexpiredate = searchParams.get('safeexpiredate');
  const restaurantName = searchParams.get('restaurant');
  const message = searchParams.get('message');

  // Restaurant data mapping
  const restaurantData = {
    wingstop: {
      name: 'Wingstop',
      discount: 'Free Fries',
      color: 'hsl(var(--wingstop-primary))',
      gradientClass: 'gradient-wingstop',
    },
    panda: {
      name: 'Panda Express',
      discount: 'Free Entree',
      color: 'hsl(var(--panda-primary))',
      gradientClass: 'gradient-panda',
    },
    rubios: {
      name: 'Rubio\'s',
      discount: 'Free Drink/Dessert',
      color: 'hsl(var(--rubios-primary))',
      gradientClass: 'gradient-rubios',
    },
    blaze: {
      name: 'Blaze Pizza',
      discount: 'Free Dessert',
      color: 'hsl(var(--blaze-primary))',
      gradientClass: 'gradient-blaze',
    }
  };

  const restaurant = restaurantName ? restaurantData[restaurantName as keyof typeof restaurantData] : null;
  
  // For Rubios, extract just the code part from the full string
  const getDisplayCode = () => {
    if (restaurantName === 'rubios' && code) {
      // Extract code from format: "Success! Online Code for a free drink or dessert with your next purchase at Rubio's: CAS32AS"
      const parts = code.split(': ');
      return parts.length > 1 ? parts[parts.length - 1].trim() : code;
    }
    return code;
  };
  
  const coupon = {
    code: getDisplayCode(),
    expirationDate: safeexpiredate,
    discount: restaurant?.discount
  };

  if ((!code && !message) || !restaurant) {
    return (
      <div className="container mx-auto px-4 py-20 text-center">
        <h1 className="text-3xl font-bold mb-4">No Coupon Found</h1>
        <p className="text-muted-foreground mb-8">
          It looks like you haven't generated a coupon yet.
        </p>
        <Button onClick={() => navigate('/')}>Back to Home</Button>
      </div>
    );
  }

  const handleCopy = async () => {
    try {
      if (coupon.code) {
        await navigator.clipboard.writeText(coupon.code);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
      }
    } catch (error) {
      console.error('Failed to copy:', error);
    }
  };

  const handleSendFeedback = async () => {
    if (!feedback.trim()) return;
    
    setSendingFeedback(true);
    try {
      const response = await fetch('/sendfeedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ feedback: feedback.trim() }),
      });

      if (response.ok) {
        toast({
          title: "Feedback sent!",
          description: "Thank you for your feedback.",
        });
        
        setFeedback('');
        setFeedbackSent(true);
      } else {
        throw new Error('Failed to send feedback');
      }
    } catch (error) {
      console.error('Failed to send feedback:', error);
      toast({
        title: "Error",
        description: "Failed to send feedback. Please try again.",
        variant: "destructive",
      });
    } finally {
      setSendingFeedback(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Success Header */}
      <section className={`${restaurant.gradientClass} py-16`}>
        <div className="container mx-auto px-4 text-center">
          <div className="max-w-2xl mx-auto text-white space-y-6">
            <div className="w-16 h-16 mx-auto bg-white/20 rounded-full flex items-center justify-center backdrop-blur-sm">
              <CheckCircle className="w-8 h-8 text-white" />
            </div>
            
            <h1 className="text-4xl font-bold">Coupon Generated Successfully!</h1>
        
          </div>
        </div>
      </section>

      {/* Coupon Display */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          {restaurant.name === 'Panda Express' ? (
            <div className="max-w-2xl mx-auto">
              {/* Thank You Header */}
              <div className="text-center mb-8">
                <div className="flex items-center justify-center mb-4">
                  <img 
                    src={pandaLogo} 
                    alt="Panda Express Logo" 
                    className="w-16 h-16 object-contain mr-4"
                  />
                  <div>
                    <h1 className="text-4xl font-bold text-red-500">THANK YOU</h1>
                    <p className="text-lg text-muted-foreground">for your feedback!</p>
                  </div>
                </div>
                <p className="text-muted-foreground">Here's a little something you can use on your next visit.</p>
              </div>

              {/* Coupon */}
              <Card className="border-2 border-red-500 border-dashed bg-white shadow-lg">
                <div className="p-8">
                  <div className="flex items-center justify-between mb-6">
                    {/* Barcode Section */}
                    <div className="flex-1">
                      {coupon.code ? (
                        <img 
                          src={`https://www.pandaguestexperience.com/Common/controls/IDAutomation/Barcode.aspx?D=${coupon.code}&LM=.25&TM=0&ST=F`}
                          alt="Present this barcode at your next in-store purchase"
                          className="w-32 h-16 object-contain"
                        />
                      ) : (
                        <div className="w-32 h-16 bg-black flex items-center justify-center">
                          <div className="text-white text-xs">|||||||||||||||</div>
                        </div>
                      )}
                      <div className="text-center mt-2">
                        <code className="text-lg font-mono font-bold">
                          {coupon.code || 'TEMPLATE123'}
                        </code>
                      </div>
                    </div>

                    {/* Offer Text */}
                    <div className="flex-2 text-center ml-8">
                      <div className="text-5xl font-bold text-red-500 mb-2">
                        FREE SMALL
                      </div>
                      <div className="text-5xl font-bold text-red-500 mb-4">
                        ENTRÉE
                      </div>
                      <div className="text-xl font-semibold text-red-500">
                        WITH PURCHASE OF
                      </div>
                      <div className="text-xl font-semibold text-red-500">
                        2-ENTRÉE PLATE
                      </div>
                    </div>
                  </div>

                  {/* Copy Button */}
                  <div className="flex justify-center mb-6">
                    <Button
                      variant="outline"
                      onClick={handleCopy}
                      className="bg-red-500 text-white hover:bg-red-600 border-red-500"
                    >
                      {copied ? (
                        <>
                          <CheckCircle className="w-4 h-4 mr-2" />
                          Copied!
                        </>
                      ) : (
                        <>
                          <Copy className="w-4 h-4 mr-2" />
                          Copy Code
                        </>
                      )}
                    </Button>
                  </div>

                  {/* Fine Print */}
                  <div className="text-xs text-muted-foreground border-t pt-4">
                    <p>Offer will expire on <strong> {safeexpiredate || '09/17/2025'}. </strong>This coupon code is good for one-time use only and is limited to one coupon code per order. <strong>Valid at participating locations and online</strong> at PandaExpress.com or on the Panda Express app.<strong> No additional charge for premium entrée. Must purchase 2-entrée plate to receive free small entrée. </strong>Delivery, tax and other fees still apply. Cannot be combined with any other offer, discount, or promotion. Cash value of 1/100 cent. Panda Restaurant Group, Inc. reserves the right to modify or discontinue the offer at any time and additional restrictions may apply.</p>
                  </div>
                </div>
              </Card>
            </div>
          ) : restaurant.name === 'Wingstop' ? (
            <div className="max-w-2xl mx-auto">
              {/* Wingstop Header with Logo */}
              <div>
                <div className="rounded-t-lg overflow-hidden">
                  <img 
                    src={wingstopBanner} 
                    alt="Wingstop Logo" 
                    className="w-full h-auto object-cover"
                  />
                </div>
              </div>

              {/* Coupon Card */}
              <Card className="border-2 border-gray-300 bg-white shadow-lg">
                <div className="p-8">
                  {/* Offer Title */}
                  <div className="text-center mb-6">
                    <h3 className="text-4xl font-black italic text-[#006341] mb-2">
                      FREE REGULAR-SIZE,
                    </h3>
                    <h3 className="text-4xl font-black italic text-[#006341] mb-4">
                      SEASONED FRY
                    </h3>
                    <p className="text-lg">
                      with your next <span className="underline font-semibold">online purchase</span> of wings or tenders.
                    </p>
                  </div>

                  {/* Divider */}
                  <div className="w-full h-1 bg-gradient-to-r from-yellow-600 via-yellow-500 to-yellow-600 mb-6"></div>

                  {/* Redemption Instructions */}
                  <div className="mb-6">
                    <p className="text-[#006341] font-semibold text-center mb-4">
                      To redeem, add the regular seasoned fry to your order and then enter the coupon code on the payment page when you order using our mobile app or <a href="https://www.wingstop.com" target="_blank" rel="noopener noreferrer" className="text-[#006341] underline hover:no-underline">wingstop.com</a>.
                    </p>
                  </div>

                  {/* Code and Expiration */}
                  <div className="bg-gray-50 p-4 rounded-lg mb-6">
                    <div className="flex items-center justify-center gap-2 mb-3">
                      <code className="text-xl font-mono font-bold">{coupon.code}</code>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={handleCopy}
                      >
                        {copied ? (
                          <CheckCircle className="w-4 h-4" />
                        ) : (
                          <Copy className="w-4 h-4" />
                        )}
                      </Button>
                    </div>
                    <div className="text-center">
                      <span className="font-bold">Expires:</span> {safeexpiredate}
                    </div>
                  </div>

                  {/* Fine Print */}
                  <div className="text-xs text-gray-600 text-center space-y-2">
                    <p>
                      Valid at participating locations only. <span className="font-semibold underline">Offer is redeemable on <a href="https://www.wingstop.com" target="_blank" rel="noopener noreferrer" className="text-gray-600 hover:text-gray-900">wingstop.com</a> or in the Wingstop mobile app only.</span>
                    </p>
                    <p>
                      Offer expires 14 days after survey completion. Limit one per customer. Offer not valid with any other offers or promotions. Other restrictions may apply.
                    </p>
                  </div>
                </div>
              </Card>
            </div>
          ) : (
            <div className="max-w-md mx-auto">
              <Card className="p-8 text-center shadow-restaurant border-border/50 bg-card/50 backdrop-blur-sm">
                <div className="space-y-6">
                  <div>
                    <Badge 
                      variant="secondary"
                      className="mb-4"
                      style={{ 
                        backgroundColor: `${restaurant.color}20`,
                        color: restaurant.color,
                        borderColor: `${restaurant.color}30`
                      }}
                    >
                      {restaurant.name}
                    </Badge>
                    
                    <h2 className="text-2xl font-bold mb-2">Your Discount</h2>
                    <div 
                      className="text-4xl font-bold mb-4"
                      style={{ color: restaurant.color }}
                    >
                      {restaurant.discount}
                    </div>
                  </div>

                  {coupon.code ? (
                    <div className="p-4 bg-muted rounded-lg">
                      <p className="text-sm text-muted-foreground mb-2">Coupon Code</p>
                      <div className="flex items-center justify-between bg-background rounded-md p-3 border">
                        <code className="text-lg font-mono font-bold">
                          {coupon.code}
                        </code>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={handleCopy}
                          className="ml-2"
                        >
                          {copied ? (
                            <CheckCircle className="w-4 h-4" />
                          ) : (
                            <Copy className="w-4 h-4" />
                          )}
                        </Button>
                      </div>
                    </div>
                  ) : message && (
                    <div className="p-4 bg-green-50 rounded-lg border border-green-200">
                      <p className="text-green-800 font-medium text-center">{message}</p>
                    </div>
                  )}

                  <div className="text-sm text-muted-foreground space-y-2">
                    <p>✅ <strong>Online Orders Only!</strong></p>
                    <p>⏰ {safeexpiredate ? `Expires on ` : 'Expires in 2 days'} <strong>{safeexpiredate}</strong></p>
                    <p>🛒 {
                      restaurantName === 'panda' ? 'Must purchase 2-entrée plate' :
                      restaurantName === 'wingstop' ? 'Valid with any online purchase (excluding drinks, sides and extras)' :
                      restaurantName === 'rubios' ? 'Valid with any online purchase (excluding drinks, sides and extras)' :
                      'Valid with any online purchase'
                    }</p>
                  </div>
                </div>
              </Card>
            </div>
          )}

          {/* Generate Another Button - Moved outside for all restaurant types */}
          <div className="flex justify-center mt-8">
            <Button
              variant="default"
              onClick={() => navigate('/')}
            >
              <Home className="w-4 h-4 mr-2" />
              Generate Another
            </Button>
          </div>
        </div>
      </section>

      {/* Instructions */}
      <section className="py-8 bg-muted/30">
        <div className="container mx-auto px-4">
          <div className="max-w-2xl mx-auto text-center">
            <h3 className="text-xl font-semibold mb-4">How to Use Your Coupon</h3>
            <div className="grid md:grid-cols-3 gap-6 text-sm">
              <div className="space-y-2">
                <div className="w-8 h-8 mx-auto rounded-full bg-primary text-primary-foreground flex items-center justify-center font-bold">
                  1
                </div>
                <p className="font-medium">
                  Visit{' '}
                  {restaurant.name === 'Panda Express' ? (
                    <a 
                      href="https://www.pandaexpress.com" 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-primary hover:underline"
                    >
                      {restaurant.name}
                    </a>
                  ) : restaurant.name === 'Wingstop' ? (
                    <a 
                      href="https://www.wingstop.com" 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-primary hover:underline"
                    >
                      {restaurant.name}
                    </a>
                  ) : restaurant.name === 'Rubio\'s' ? (
                    <a 
                      href="https://www.rubios.com" 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-primary hover:underline"
                    >
                      {restaurant.name}
                    </a>
                  ) : restaurant.name === 'Blaze Pizza' ? (
                    <a 
                      href="https://www.blazepizza.com" 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-primary hover:underline"
                    >
                      {restaurant.name}
                    </a>
                  ) : (
                    restaurant.name
                  )}
                </p>
                <p className="text-muted-foreground">
                  {restaurant.name === 'Panda Express' ? 'Online or In-Store' : 'Online Only'}
                </p>
              </div>
              
              <div className="space-y-2">
                <div className="w-8 h-8 mx-auto rounded-full bg-primary text-primary-foreground flex items-center justify-center font-bold">
                  2
                </div>
                <p className="font-medium">Add All Required Items</p>
                <p className="text-muted-foreground">To Order</p>
              </div>
              
              <div className="space-y-2">
                <div className="w-8 h-8 mx-auto rounded-full bg-primary text-primary-foreground flex items-center justify-center font-bold">
                  3
                </div>
                <p className="font-medium">
                  {restaurant.name === 'Panda Express' ? 'Enter/Show Coupon Code' : 'Enter Coupon Code'}
                </p>
                <p className="text-muted-foreground">At Checkout</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Feedback Section */}
      {!feedbackSent && (
        <section className="py-8 bg-background">
          <div className="container mx-auto px-4">
            <div className="max-w-md mx-auto">
              <Card className="p-6">
                <div className="space-y-4">
                  <div className="text-center">
                    <h3 className="text-lg font-semibold mb-2">Share Your Experience</h3>

                  </div>
                  
                  <Textarea
                    placeholder="W or L revamp..."
                    value={feedback}
                    onChange={(e) => setFeedback(e.target.value)}
                    className="min-h-[100px]"
                  />
                  
                  <Button
                    onClick={handleSendFeedback}
                    disabled={!feedback.trim() || sendingFeedback}
                    className="w-full"
                  >
                    {sendingFeedback ? (
                      <>
                        <div className="w-4 h-4 mr-2 animate-spin rounded-full border-2 border-background border-t-transparent"></div>
                        Sending...
                      </>
                    ) : (
                      <>
                        <Send className="w-4 h-4 mr-2" />
                        Send Feedback
                      </>
                    )}
                  </Button>
                </div>
              </Card>
            </div>
          </div>
        </section>
      )}
    </div>
  );
};

export default ResultPage;