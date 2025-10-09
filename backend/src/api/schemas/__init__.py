"""
Pydantic schemas package for API request/response models.

This module organizes all Pydantic schemas for the betting platform API,
providing consistent validation and serialization across all endpoints.
"""

from .user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserPasswordUpdate,
    UserResponse,
    UserProfile,
    UserSummary,
    UserLogin,
    UserLoginResponse,
    UserRegistrationResponse
)

from .group import (
    GroupBase,
    GroupCreate,
    GroupUpdate,
    GroupResponse,
    GroupSummary,
    GroupWithStats
)

from .sport import (
    SportBase,
    SportCreate,
    SportUpdate,
    SportResponse,
    SportSummary,
    SportWithStats
)

from .team import (
    TeamBase,
    TeamCreate,
    TeamUpdate,
    TeamResponse,
    TeamSummary,
    TeamWithStats,
    TeamWithSport
)

from .competition import (
    CompetitionBase,
    CompetitionCreate,
    CompetitionUpdate,
    CompetitionResponse,
    CompetitionSummary,
    CompetitionWithStats,
    CompetitionWithSport,
    CompetitionTeamRegistration,
    CompetitionTeamList,
    CompetitionStatus,
    CompetitionFormat
)

from .season import (
    SeasonBase,
    SeasonCreate,
    SeasonUpdate,
    SeasonResponse,
    SeasonSummary,
    SeasonWithStats,
    SeasonCompetitionList,
    SeasonStandings,
    SeasonStatus,
    SeasonType
)

from .bet import (
    BetBase,
    BetCreate,
    BetUpdate,
    BetResponse,
    BetSummary,
    BetWithMatch,
    BetWithUser,
    BetWithStats,
    BetHistory,
    BetSettlement,
    BetSlip,
    BetLeaderboard,
    BetType,
    BetStatus,
    BetOutcome
)

from .result import (
    ResultCreate,
    ResultUpdate,
    ResultResponse,
    ResultSummary,
    ResultWithMatch,
    ResultWithDetails,
    ResultHistory,
    ResultStatistics,
    ResultOutcome,
    ResultValidation,
    ResultConfirmation,
    ResultDispute,
    ResultAnalytics,
    ResultBulkCreate,
    ResultBulkResponse
)

from .group_membership import (
    GroupMembershipCreate,
    GroupMembershipUpdate,
    GroupMembershipResponse,
    GroupMembershipSummary,
    GroupMembershipWithUser,
    GroupMembershipWithGroup,
    GroupMembershipWithDetails,
    GroupInvitation,
    GroupJoinRequest,
    MembershipApproval,
    MembershipRoleUpdate,
    OwnershipTransfer,
    GroupMembershipStatistics,
    GroupMembershipHistory,
    GroupMembershipBulkCreate,
    GroupMembershipBulkResponse,
    GroupLeaveRequest,
    GroupMembershipFilters,
    MembershipStatus,
    MembershipRole,
    InvitationType
)

from .audit_log import (
    AuditLogCreate,
    AuditLogUpdate,
    AuditLogResponse,
    AuditLogSummary,
    AuditLogWithUser,
    AuditLogWithEntity,
    AuditLogWithDetails,
    AuditLogFilters,
    AuditLogStatistics,
    AuditLogAnalytics,
    AuditLogExport,
    AuditLogExportResponse,
    AuditLogBulkCreate,
    AuditLogBulkResponse,
    AuditLogArchive,
    AuditLogArchiveResponse,
    ActionType,
    EntityType,
    LogLevel
)

__all__ = [
    # User schemas
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserPasswordUpdate",
    "UserResponse",
    "UserProfile",
    "UserSummary",
    "UserLogin",
    "UserLoginResponse",
    "UserRegistrationResponse",
    
    # Group schemas
    "GroupBase",
    "GroupCreate",
    "GroupUpdate",
    "GroupResponse",
    "GroupSummary",
    "GroupWithStats",
    
    # Sport schemas
    "SportBase",
    "SportCreate",
    "SportUpdate",
    "SportResponse",
    "SportSummary",
    "SportWithStats",
    
    # Team schemas
    "TeamBase",
    "TeamCreate",
    "TeamUpdate",
    "TeamResponse",
    "TeamSummary",
    "TeamWithStats",
    "TeamWithSport",
    
    # Competition schemas
    "CompetitionBase",
    "CompetitionCreate",
    "CompetitionUpdate",
    "CompetitionResponse",
    "CompetitionSummary",
    "CompetitionWithStats",
    "CompetitionWithSport",
    "CompetitionTeamRegistration",
    "CompetitionTeamList",
    "CompetitionStatus",
    "CompetitionFormat",
    
    # Season schemas
    "SeasonBase",
    "SeasonCreate",
    "SeasonUpdate",
    "SeasonResponse",
    "SeasonSummary",
    "SeasonWithStats",
    "SeasonCompetitionList",
    "SeasonStandings",
    "SeasonStatus",
    "SeasonType",
    
    # Bet schemas
    "BetBase",
    "BetCreate",
    "BetUpdate",
    "BetResponse",
    "BetSummary",
    "BetWithMatch",
    "BetWithUser",
    "BetWithStats",
    "BetHistory",
    "BetSettlement",
    "BetSlip",
    "BetLeaderboard",
    "BetType",
    "BetStatus",
    "BetOutcome",
    
    # Result schemas
    "ResultCreate",
    "ResultUpdate",
    "ResultResponse",
    "ResultSummary",
    "ResultWithMatch",
    "ResultWithDetails",
    "ResultHistory",
    "ResultStatistics",
    "ResultOutcome",
    "ResultValidation",
    "ResultConfirmation",
    "ResultDispute",
    "ResultAnalytics",
    "ResultBulkCreate",
    "ResultBulkResponse",
    
    # Group Membership schemas
    "GroupMembershipCreate",
    "GroupMembershipUpdate",
    "GroupMembershipResponse",
    "GroupMembershipSummary",
    "GroupMembershipWithUser",
    "GroupMembershipWithGroup",
    "GroupMembershipWithDetails",
    "GroupInvitation",
    "GroupJoinRequest",
    "MembershipApproval",
    "MembershipRoleUpdate",
    "OwnershipTransfer",
    "GroupMembershipStatistics",
    "GroupMembershipHistory",
    "GroupMembershipBulkCreate",
    "GroupMembershipBulkResponse",
    "GroupLeaveRequest",
    "GroupMembershipFilters",
    "MembershipStatus",
    "MembershipRole",
    "InvitationType",
    
    # Audit Log schemas
    "AuditLogCreate",
    "AuditLogUpdate",
    "AuditLogResponse",
    "AuditLogSummary",
    "AuditLogWithUser",
    "AuditLogWithEntity",
    "AuditLogWithDetails",
    "AuditLogFilters",
    "AuditLogStatistics",
    "AuditLogAnalytics",
    "AuditLogExport",
    "AuditLogExportResponse",
    "AuditLogBulkCreate",
    "AuditLogBulkResponse",
    "AuditLogArchive",
    "AuditLogArchiveResponse",
    "ActionType",
    "EntityType",
    "LogLevel",
]