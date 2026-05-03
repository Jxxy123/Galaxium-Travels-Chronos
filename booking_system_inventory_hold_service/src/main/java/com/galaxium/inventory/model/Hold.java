package com.galaxium.inventory.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.Instant;

@Entity
@Table(name = "holds")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Hold {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @JsonProperty("holdId")
    private Long id;

    
    @Column(nullable = false)
    private Integer flightId;
    
    @Column(nullable = false)
    private String seatClass;
    
    @Column(nullable = false)
    private Integer quantity;
    
    @Column(nullable = false)
    private Double pricePerSeat;
    
    @Column(nullable = false)
    private Double totalPrice;
    
    @Column(nullable = false)
    private Instant expiresAt;
    
    @Column(nullable = false)
    private Instant createdAt;
    
    @Column(nullable = false)
    private String status; // ACTIVE, EXPIRED, RELEASED
}

// Made with Bob
