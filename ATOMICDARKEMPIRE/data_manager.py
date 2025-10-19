"""
🌑 DATA MANAGER
Handles all JSON data storage for economy, teams, marketplace, and moderation
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional


class DataManager:
    def __init__(self):
        self.data_dir = 'data'
        self.economy_file = os.path.join(self.data_dir, 'economy.json')
        self.teams_file = os.path.join(self.data_dir, 'teams.json')
        self.market_file = os.path.join(self.data_dir, 'market.json')
        self.moderation_file = os.path.join(self.data_dir, 'moderation.json')
        
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Load all data
        self.economy = self._load_json(self.economy_file, {})
        self.teams = self._load_json(self.teams_file, self._init_teams_data())
        self.market = self._load_json(self.market_file, {'listings': [], 'next_id': 1})
        self.moderation = self._load_json(self.moderation_file, {'logs': []})
    
    def _load_json(self, filepath: str, default: Any) -> Any:
        """Load JSON file or return default"""
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return default
        return default
    
    def _save_json(self, filepath: str, data: Any):
        """Save data to JSON file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _init_teams_data(self) -> Dict:
        """Initialize teams data structure"""
        teams = {}
        team_ids = [
            'blood_vampires', 'shadow_phantoms', 'toxic_mutants', 'soul_collectors',
            'dark_warlocks', 'hellfire_demons', 'void_reapers', 'ghost_apparitions',
            'nightmare_creatures', 'crystal_wraiths', 'abyssal_horrors', 'volcanic_demons',
            'storm_horrors', 'cosmic_terrors', 'lunar_cults', 'eclipse_cults',
            'forest_haunts', 'mountain_wraiths', 'inferno_lords', 'frost_specters'
        ]
        
        for team_id in team_ids:
            teams[team_id] = {
                'lord': None,
                'lord_hand': None,
                'members': [],
                'vault': {
                    'soul_fragments': 0,
                    'cursed_essence': 0,
                    'tombstone_coins': 0,
                    'lords_blood': 0,
                    'void_crystals': 0
                },
                'join_requests': []
            }
        return teams
    
    # ========== ECONOMY FUNCTIONS ==========
    
    def init_user(self, user_id: int):
        """Initialize user if not exists"""
        user_id_str = str(user_id)
        if user_id_str not in self.economy:
            self.economy[user_id_str] = {
                'currencies': {
                    'soul_fragments': 0,
                    'cursed_essence': 0,
                    'tombstone_coins': 0,
                    'lords_blood': 0,
                    'void_crystals': 0
                },
                'level': 1,
                'xp': 0,
                'prestige': 0,
                'messages': 0,
                'daily_streak': 0,
                'last_daily': None,
                'team': None
            }
            self.save_economy()
    
    def get_user(self, user_id: int) -> Dict:
        """Get user data"""
        self.init_user(user_id)
        return self.economy[str(user_id)]
    
    def save_economy(self):
        """Save economy data"""
        self._save_json(self.economy_file, self.economy)
    
    def get_leaderboard(self, limit: int = 10) -> list:
        """Get wealth leaderboard"""
        users = []
        for user_id, data in self.economy.items():
            total_wealth = sum(data['currencies'].values())
            users.append({
                'user_id': int(user_id),
                'total_wealth': total_wealth,
                'soul_fragments': data['currencies']['soul_fragments'],
                'level': data['level']
            })
        
        users.sort(key=lambda x: x['total_wealth'], reverse=True)
        return users[:limit]
    
    # ========== TEAM FUNCTIONS ==========
    
    def get_team(self, team_id: str) -> Optional[Dict]:
        """Get team data"""
        return self.teams.get(team_id)
    
    def get_user_team(self, user_id: int) -> Optional[str]:
        """Get user's team ID"""
        user_data = self.get_user(user_id)
        return user_data.get('team')
    
    def join_team(self, user_id: int, team_id: str) -> bool:
        """Add user to team"""
        if team_id not in self.teams:
            return False
        
        team = self.teams[team_id]
        user_id_int = int(user_id)
        
        if user_id_int not in team['members']:
            team['members'].append(user_id_int)
            self.economy[str(user_id)]['team'] = team_id
            self.save_teams()
            self.save_economy()
            return True
        return False
    
    def leave_team(self, user_id: int, team_id: str) -> bool:
        """Remove user from team"""
        if team_id not in self.teams:
            return False
        
        team = self.teams[team_id]
        user_id_int = int(user_id)
        
        if user_id_int in team['members']:
            team['members'].remove(user_id_int)
            self.economy[str(user_id)]['team'] = None
            self.save_teams()
            self.save_economy()
            return True
        return False
    
    def add_join_request(self, user_id: int, team_id: str):
        """Add join request to team"""
        if team_id in self.teams:
            user_id_int = int(user_id)
            if user_id_int not in self.teams[team_id]['join_requests']:
                self.teams[team_id]['join_requests'].append(user_id_int)
                self.save_teams()
    
    def remove_join_request(self, user_id: int, team_id: str):
        """Remove join request"""
        if team_id in self.teams:
            user_id_int = int(user_id)
            if user_id_int in self.teams[team_id]['join_requests']:
                self.teams[team_id]['join_requests'].remove(user_id_int)
                self.save_teams()
    
    def save_teams(self):
        """Save teams data"""
        self._save_json(self.teams_file, self.teams)
    
    def get_team_leaderboard(self) -> list:
        """Get team wealth leaderboard"""
        teams_list = []
        for team_id, team_data in self.teams.items():
            total_wealth = sum(team_data['vault'].values())
            teams_list.append({
                'team_id': team_id,
                'total_wealth': total_wealth,
                'members': len(team_data['members']),
                'lord': team_data['lord']
            })
        
        teams_list.sort(key=lambda x: x['total_wealth'], reverse=True)
        return teams_list
    
    # ========== MARKETPLACE FUNCTIONS ==========
    
    def create_listing(self, seller_id: int, price: int, currency: str, item_name: str) -> int:
        """Create marketplace listing"""
        listing_id = self.market['next_id']
        self.market['listings'].append({
            'id': listing_id,
            'seller_id': seller_id,
            'price': price,
            'currency': currency,
            'item_name': item_name,
            'created_at': datetime.now().isoformat(),
            'verified': False
        })
        self.market['next_id'] += 1
        self.save_market()
        return listing_id
    
    def get_listing(self, listing_id: int) -> Optional[Dict]:
        """Get listing by ID"""
        for listing in self.market['listings']:
            if listing['id'] == listing_id:
                return listing
        return None
    
    def remove_listing(self, listing_id: int) -> bool:
        """Remove listing"""
        for i, listing in enumerate(self.market['listings']):
            if listing['id'] == listing_id:
                self.market['listings'].pop(i)
                self.save_market()
                return True
        return False
    
    def get_user_listings(self, user_id: int) -> list:
        """Get user's listings"""
        return [l for l in self.market['listings'] if l['seller_id'] == user_id]
    
    def save_market(self):
        """Save marketplace data"""
        self._save_json(self.market_file, self.market)
    
    # ========== MODERATION FUNCTIONS ==========
    
    def log_moderation(self, action: str, moderator_id: int, target_id: int, reason: Optional[str] = None):
        """Log moderation action"""
        self.moderation['logs'].append({
            'action': action,
            'moderator_id': moderator_id,
            'target_id': target_id,
            'reason': reason,
            'timestamp': datetime.now().isoformat()
        })
        self.save_moderation()
    
    def save_moderation(self):
        """Save moderation data"""
        self._save_json(self.moderation_file, self.moderation)
