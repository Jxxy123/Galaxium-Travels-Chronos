import type { Flight, SeatClass } from '../../types';
import { Card, Button } from '../common';
import { Plane, Clock, Users, Crown, Rocket, Zap } from 'lucide-react';
import { formatCurrency, formatDate, formatTime, calculateDuration } from '../../utils/formatters';
import { motion } from 'framer-motion';
import { useState } from 'react';

interface FlightCardProps {
  flight: Flight;
  onBook: (flight: Flight) => void;
}

export const FlightCard = ({ flight, onBook }: FlightCardProps) => {
  const [showPhysics, setShowPhysics] = useState(false);
  const totalSeats = flight.economy_seats_available + flight.business_seats_available + flight.galaxium_seats_available;
  const isSoldOut = totalSeats === 0;
  const isRelativisticSpeed = flight.velocity > 0.7;

  const seatClasses = [
    {
      name: 'Economy',
      class: 'economy' as SeatClass,
      price: flight.economy_price,
      seats: flight.economy_seats_available,
      icon: Plane,
      color: 'text-blue-400',
      bgColor: 'bg-blue-500/10',
      borderColor: 'border-blue-500/30',
    },
    {
      name: 'Business',
      class: 'business' as SeatClass,
      price: flight.business_price,
      seats: flight.business_seats_available,
      icon: Crown,
      color: 'text-purple-400',
      bgColor: 'bg-purple-500/10',
      borderColor: 'border-purple-500/30',
    },
    {
      name: 'Galaxium Class',
      class: 'galaxium' as SeatClass,
      price: flight.galaxium_price,
      seats: flight.galaxium_seats_available,
      icon: Rocket,
      color: 'text-alien-green',
      bgColor: 'bg-alien-green/10',
      borderColor: 'border-alien-green/30',
    },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -4 }}
      transition={{ duration: 0.3 }}
    >
      <Card className="h-full flex flex-col">
        {/* Route Header */}
        <div className="flex items-center justify-between mb-4 pb-4 border-b border-white/10">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-cosmic-gradient">
              <Plane className="text-white" size={24} />
            </div>
            <div>
              <h3 className="text-xl font-bold text-star-white">
                {flight.origin} → {flight.destination}
              </h3>
              <p className="text-sm text-star-white/60">
                Flight #{flight.flight_id}
              </p>
            </div>
          </div>
        </div>

        {/* Flight Details */}
        <div className="space-y-4 mb-6 flex-1">
          {/* Departure & Arrival */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-xs text-star-white/60 mb-1">Departure</p>
              <p className="text-sm font-medium text-star-white">
                {formatDate(flight.departure_time, 'MMM dd, yyyy')}
              </p>
              <p className="text-lg font-bold text-cosmic-purple">
                {formatTime(flight.departure_time)}
              </p>
            </div>
            <div>
              <p className="text-xs text-star-white/60 mb-1">Arrival</p>
              <p className="text-sm font-medium text-star-white">
                {formatDate(flight.arrival_time, 'MMM dd, yyyy')}
              </p>
              <p className="text-lg font-bold text-cosmic-purple">
                {formatTime(flight.arrival_time)}
              </p>
            </div>
          </div>

          {/* Duration and Relativistic Badge */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-star-white/70">
              <Clock size={16} />
              <span className="text-sm">
                Duration: {calculateDuration(flight.departure_time, flight.arrival_time)}
              </span>
            </div>
            {isRelativisticSpeed && (
              <div className="flex items-center gap-1 px-2 py-1 rounded-full bg-solar-orange/20 border border-solar-orange/40">
                <Zap size={14} className="text-solar-orange" />
                <span className="text-xs font-semibold text-solar-orange">Relativistic Speed</span>
              </div>
            )}
          </div>

          {/* Time Dilation Physics Section */}
          {flight.velocity > 0 && (
            <div className="border border-cosmic-purple/30 rounded-lg overflow-hidden">
              <button
                onClick={() => setShowPhysics(!showPhysics)}
                className="w-full px-3 py-2 bg-cosmic-purple/10 hover:bg-cosmic-purple/20 transition-colors flex items-center justify-between"
              >
                <span className="text-sm font-medium text-cosmic-purple">
                  ⚛️ Physics Details {showPhysics ? '▼' : '▶'}
                </span>
              </button>
              
              {showPhysics && (
                <div className="p-3 space-y-2 bg-space-black/50">
                  <div className="text-xs text-star-white/80">
                    <div className="mb-2">
                      <span className="font-semibold text-cosmic-purple">Velocity:</span>{' '}
                      {(flight.velocity * 100).toFixed(1)}% of light speed
                    </div>
                    
                    <div className="mb-2 p-2 bg-cosmic-purple/10 rounded border border-cosmic-purple/30">
                      <div className="font-semibold text-alien-green mb-1">
                        Lorentz Factor (γ): {flight.lorentz_factor.toFixed(3)}
                      </div>
                      <div className="text-xs text-star-white/60">
                        γ = 1/√(1 - v²/c²)
                      </div>
                    </div>
                    
                    <div className="mb-2 p-2 bg-blue-500/10 rounded border border-blue-400/30">
                      <div className="font-semibold text-blue-400 mb-1">
                        Time Dilation Factor: {flight.time_dilation_factor.toFixed(3)}
                      </div>
                      <div className="text-xs text-star-white/60">
                        Time passes {flight.time_dilation_factor.toFixed(3)}× slower on ship
                      </div>
                    </div>
                    
                    <div className="space-y-1 mb-2">
                      <div>
                        <span className="font-semibold text-blue-400">Ship Time:</span>{' '}
                        {flight.proper_time_hours.toFixed(2)} hours
                      </div>
                      <div>
                        <span className="font-semibold text-purple-400">Earth Time:</span>{' '}
                        {(flight.proper_time_hours / flight.time_dilation_factor).toFixed(2)} hours
                      </div>
                    </div>
                    
                    <div className="text-xs text-star-white/60 italic border-t border-white/10 pt-2">
                      ℹ️ For every 1 hour onboard, {(1 / flight.time_dilation_factor).toFixed(2)} hours pass on Earth due to relativistic time dilation.
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Seat Classes */}
          <div className="space-y-2">
            <p className="text-xs text-star-white/60 mb-2">Available Seat Classes</p>
            {seatClasses.map((seatClass) => {
              const Icon = seatClass.icon;
              const isClassSoldOut = seatClass.seats === 0;
              const isLowSeats = seatClass.seats <= 2 && seatClass.seats > 0;
              
              return (
                <div
                  key={seatClass.class}
                  className={`p-3 rounded-lg border ${seatClass.borderColor} ${seatClass.bgColor} ${
                    isClassSoldOut ? 'opacity-50' : ''
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Icon size={18} className={seatClass.color} />
                      <span className="font-medium text-star-white">{seatClass.name}</span>
                    </div>
                    <div className="text-right">
                      <div className={`text-lg font-bold ${seatClass.color}`}>
                        {formatCurrency(seatClass.price)}
                      </div>
                      <div className="flex items-center gap-1 text-xs">
                        <Users size={12} className={isLowSeats ? 'text-solar-orange' : 'text-star-white/60'} />
                        <span className={isLowSeats ? 'text-solar-orange font-semibold' : 'text-star-white/60'}>
                          {isClassSoldOut ? 'Sold Out' : `${seatClass.seats} left`}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Book Button */}
        <Button
          onClick={() => onBook(flight)}
          disabled={isSoldOut}
          className="w-full"
        >
          {isSoldOut ? 'All Classes Sold Out' : 'Select Seat Class'}
        </Button>
      </Card>
    </motion.div>
  );
};

// Made with Bob
