package com.example.BaseballAI.repository;

import com.example.BaseballAI.domain.RankingItem;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface RankingItemRepository extends JpaRepository<RankingItem, Long> {
    // rank 순으로 정렬해서 가져오는 커스텀 메소드 예시
    List<RankingItem> findAllByOrderByRankAsc();
}