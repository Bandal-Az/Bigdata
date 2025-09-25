package com.example.BaseballAI.repository;

import com.example.BaseballAI.domain.GameScheduleItem;
import org.springframework.data.jpa.repository.JpaRepository; // JpaRepository로 변경
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface GameScheduleItemRepository extends JpaRepository<GameScheduleItem, Long> { // ID 타입을 Long으로 변경
    // 특정 날짜 경기 조회
    // 쿼리 메소드 이름은 JPA 규칙을 따라야 해!
    // JPA는 컬럼명에 언더스코어(_)가 있어도 카멜케이스(CamelCase)로 인식해줘.
    List<GameScheduleItem> findByTimeContaining(String date);
}
