package com.galaxium.inventory.repository;

import com.galaxium.inventory.model.Hold;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.Instant;
import java.util.List;

@Repository
public interface HoldRepository extends JpaRepository<Hold, Long> {
    List<Hold> findByFlightIdAndSeatClassAndStatus(Integer flightId, String seatClass, String status);
    List<Hold> findByStatusAndExpiresAtBefore(String status, Instant now);
}

// Made with Bob
