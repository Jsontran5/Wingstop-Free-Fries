import { Link } from 'react-router-dom';
import { useEffect } from 'react';
import eggImage from '@/assets/egg.png';

const ErrorPage = () => {
  useEffect(() => {
    document.title = 'Error: Restricted Email';
  }, []);

  return (
    <div style={{ 
      margin: 0, 
      padding: 0, 
      boxSizing: 'border-box',
      backgroundColor: 'white',
      minHeight: '100vh',
      fontFamily: 'Arial, sans-serif'
    }}>
      <img 
        src={eggImage} 
        alt="Error Image" 
        style={{ textAlign: 'center' }} 
      />
      <p style={{ textAlign: 'center' }}>
        <Link to="/" style={{ color: 'blue', textDecoration: 'none' }}>
          Back to Safety
        </Link>
      </p>

      {/* <div 
        style={{
          position: 'fixed',
          bottom: '350px',
          left: '50%',
          transform: 'translateX(-50%)',
          backgroundColor: 'red',
          color: 'white',
          padding: '10px',
          borderRadius: '5px'
        }}
      >
        Again, the site's functionality is currently broken ☹️.<br /> 
        Email me at <a href="mailto:foodsurveycodes@gmail.com" style={{ color: 'white' }}> foodsurveycodes@gmail.com </a> if you need a coupon.
      </div> */}
      
      {/* CSS styles from original HTML (kept for exact replication but unused) */}
      <style>{`
        * {
          margin: 0;
          padding: 0;
          box-sizing: border-box;
        }
        .navbar {
          background-color: #333;
          overflow: hidden;
          list-style: none;
        }
        .nav-item {
          float: left;
        }
        .nav-item a {
          display: block;
          color: white;
          text-align: center;
          padding: 14px 16px;
          text-decoration: none;
        }
        .nav-item a:hover {
          background-color: #ddd;
          color: black;
        }
        footer {
          color: black;
          text-align: center;
          padding: 10px;
          position: fixed;
          bottom: 0;
          width: 100%;
          background-color: transparent;
        }
        footer a {
          color: blue;
          text-decoration: none;
        }
        .site-down-note {
          position: fixed;
          bottom: 350px;
          left: 50%;
          transform: translateX(-50%);
          background-color: red;
          color: white;
          padding: 10px;
          border-radius: 5px;
        }
      `}</style>
    </div>
  );
};

export default ErrorPage;
