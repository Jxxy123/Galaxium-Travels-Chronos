package com.galaxium.inventory.controller;

import com.galaxium.inventory.model.Hold;
import com.galaxium.inventory.service.HoldService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/v1")
@CrossOrigin(origins = "*")
public class HoldController {
    
    @Autowired
    private HoldService holdService;
    
    @GetMapping("/health")
    public ResponseEntity<Map<String, String>> health() {
        return ResponseEntity.ok(Map.of("status", "UP"));
    }
    
    @PostMapping("/holds")
    public ResponseEntity<Hold> createHold(@RequestBody Map<String, Object> request) {
        Integer flightId = (Integer) request.get("flight_id");
        String seatClass = (String) request.get("seat_class");
        Integer quantity = (Integer) request.get("quantity");
        Integer durationMinutes = (Integer) request.getOrDefault("duration_minutes", 15);
        Double pricePerSeat = ((Number) request.get("price_per_seat")).doubleValue();
        Double totalPrice = ((Number) request.get("total_price")).doubleValue();
        
        Hold hold = holdService.createHold(flightId, seatClass, quantity, durationMinutes, pricePerSeat, totalPrice);
        return ResponseEntity.ok(hold);
    }
    
    @GetMapping("/holds/{holdId}")
    public ResponseEntity<Hold> getHold(@PathVariable Long holdId) {
        Hold hold = holdService.getHold(holdId);
        if (hold == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(hold);
    }
    
    @PostMapping("/holds/{holdId}/confirm")
    public ResponseEntity<Hold> confirmHold(@PathVariable Long holdId) {
        Hold hold = holdService.getHold(holdId);
        if (hold == null) {
            return ResponseEntity.notFound().build();
        }
        // In a real system, this would create a booking in the main system
        // For now, we'll just mark it as confirmed by changing status
        hold.setStatus("CONFIRMED");
        holdService.confirmHold(holdId);
        return ResponseEntity.ok(hold);
    }
    
    @PostMapping("/holds/{holdId}/release")
    public ResponseEntity<Map<String, String>> releaseHold(@PathVariable Long holdId) {
        holdService.releaseHold(holdId);
        return ResponseEntity.ok(Map.of("status", "released"));
    }
    
    @DeleteMapping("/holds/{holdId}")
    public ResponseEntity<Map<String, String>> deleteHold(@PathVariable Long holdId) {
        holdService.releaseHold(holdId);
        return ResponseEntity.ok(Map.of("status", "released"));
    }
    
    @GetMapping("/holds/count")
    public ResponseEntity<Map<String, Integer>> getHoldCount(
            @RequestParam Integer flightId,
            @RequestParam String seatClass) {
        int count = holdService.getActiveHoldCount(flightId, seatClass);
        return ResponseEntity.ok(Map.of("active_holds", count));
    }
}

// Made with Bob
