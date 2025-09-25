package com.example.BaseballAI.service;

import com.example.BaseballAI.domain.GameScheduleItem;
import com.example.BaseballAI.repository.GameScheduleItemRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class GameScheduleService {

    private final GameScheduleItemRepository scheduleRepository;

    public GameScheduleService(GameScheduleItemRepository scheduleRepository) {
        this.scheduleRepository = scheduleRepository;
    }

    public void saveAll(List<GameScheduleItem> schedules) {
        scheduleRepository.saveAll(schedules);
    }

    public List<GameScheduleItem> getAll() {
        return scheduleRepository.findAll();
    }
}
