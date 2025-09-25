package com.example.BaseballAI.dto.Crawling;

import lombok.Data;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@Data
public class GameScheduleItemDTO {
    private String time;
    private String home_team;
    private String away_team;
    private String stadium;
    private String status;
    private Integer home_score;     // null 가능 -> Integer
    private Integer away_score;     // null 가능 -> Integer
    private String home_pitcher;    // null 가능
    private String away_pitcher;    // null 가능
    private String winner;          // null 가능
}