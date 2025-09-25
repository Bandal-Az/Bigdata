package com.example.BaseballAI.dto.Crawling;

import lombok.Data;
import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
@Data
public class RankingItemDTO {
    private int rank;
    private String name;
    private int games;
    private int wins;
    private int losses;
    private int draws;
    private double win_rate;
}