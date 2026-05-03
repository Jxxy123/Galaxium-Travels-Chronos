package com.galaxium.inventory.service;

import com.galaxium.inventory.model.Hold;
import com.galaxium.inventory.repository.HoldRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.List;

@Service
public class HoldService {
    
    @Autowired
    private HoldRepository holdRepository;
    
    @Transactional
    public Hold createHold(Integer flightId, String seatClass, Integer quantity, int durationMinutes, Double pricePerSeat, Double totalPrice) {
        Hold hold = new Hold();
        hold.setFlightId(flightId);
        hold.setSeatClass(seatClass);
        hold.setQuantity(quantity);
        hold.setPricePerSeat(pricePerSeat);
        hold.setTotalPrice(totalPrice);
        hold.setCreatedAt(Instant.now());
        hold.setExpiresAt(Instant.now().plus(durationMinutes, ChronoUnit.MINUTES));
        hold.setStatus("ACTIVE");
        
        return holdRepository.save(hold);
    }
    
    public Hold getHold(Long holdId) {
        return holdRepository.findById(holdId).orElse(null);
    }
    
    @Transactional
    public void confirmHold(Long holdId) {
        holdRepository.findById(holdId).ifPresent(hold -> {
            hold.setStatus("CONFIRMED");
            holdRepository.save(hold);
        });
    }
    
    @Transactional
    public void releaseHold(Long holdId) {
        holdRepository.findById(holdId).ifPresent(hold -> {
            hold.setStatus("RELEASED");
            holdRepository.save(hold);
        });
    }
    
    public int getActiveHoldCount(Integer flightId, String seatClass) {
        List<Hold> activeHolds = holdRepository.findByFlightIdAndSeatClassAndStatus(
            flightId, seatClass, "ACTIVE"
        );
        return activeHolds.stream()
            .filter(hold -> hold.getExpiresAt().isAfter(Instant.now()))
            .mapToInt(Hold::getQuantity)
            .sum();
    }
    
    @Scheduled(fixedRate = 60000) // Run every minute
    @Transactional
    public void expireOldHolds() {
        List<Hold> expiredHolds = holdRepository.findByStatusAndExpiresAtBefore(
            "ACTIVE", Instant.now()
        );
        expiredHolds.forEach(hold -> {
            hold.setStatus("EXPIRED");
            holdRepository.save(hold);
        });
    }
}

// Made with Bob
