package com.example.BaseballAI.domain;

import jakarta.persistence.*; // JPA 사용을 위해 import
import java.io.Serializable;

// 롬복(@Getter, @Setter)을 사용하면 더 깔끔하게 코드를 만들 수 있어!
@Entity // 이 클래스가 JPA 엔티티임을 명시
@Table(name = "game_schedule") // 매핑될 테이블 이름 지정
public class GameScheduleItem implements Serializable {
    @Id // 기본 키(Primary Key) 지정
    @GeneratedValue(strategy = GenerationType.IDENTITY) // DB에서 ID를 자동으로 생성
    private Long id; // ID 타입을 Long으로 변경

    // OracleDB의 컬럼명은 소문자와 언더스코어(_)를 사용하도록 맞춰주는 게 좋아!
    @Column(name = "time")
    private String time;

    @Column(name = "home_team")
    private String home_team;

    @Column(name = "away_team")
    private String away_team;

    @Column(name = "stadium")
    private String stadium;

    @Column(name = "status")
    private String status;

    @Column(name = "home_score")
    private Integer home_score;     // null 가능

    @Column(name = "away_score")
    private Integer away_score;     // null 가능

    @Column(name = "home_pitcher")
    private String home_pitcher;    // null 가능

    @Column(name = "away_pitcher")
    private String away_pitcher;    // null 가능

    @Column(name = "winner")
    private String winner;         // null 가능

    // 생성자, Getter, Setter는 롬복을 사용하면 코드가 훨씬 예뻐져!
    // 아래는 롬복이 없을 때의 코드
    public GameScheduleItem() {
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getTime() {
        return time;
    }

    public void setTime(String time) {
        this.time = time;
    }

    public String getHome_team() {
        return home_team;
    }

    public void setHome_team(String home_team) {
        this.home_team = home_team;
    }

    public String getAway_team() {
        return away_team;
    }

    public void setAway_team(String away_team) {
        this.away_team = away_team;
    }

    public String getStadium() {
        return stadium;
    }

    public void setStadium(String stadium) {
        this.stadium = stadium;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public Integer getHome_score() {
        return home_score;
    }

    public void setHome_score(Integer home_score) {
        this.home_score = home_score;
    }

    public Integer getAway_score() {
        return away_score;
    }

    public void setAway_score(Integer away_score) {
        this.away_score = away_score;
    }

    public String getHome_pitcher() {
        return home_pitcher;
    }

    public void setHome_pitcher(String home_pitcher) {
        this.home_pitcher = home_pitcher;
    }

    public String getAway_pitcher() {
        return away_pitcher;
    }

    public void setAway_pitcher(String away_pitcher) {
        this.away_pitcher = away_pitcher;
    }

    public String getWinner() {
        return winner;
    }

    public void setWinner(String winner) {
        this.winner = winner;
    }
}