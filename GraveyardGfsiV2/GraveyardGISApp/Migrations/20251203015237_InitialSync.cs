using System;
using Microsoft.EntityFrameworkCore.Metadata;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace GraveyardGISApp.Migrations
{
    /// <inheritdoc />
    public partial class InitialSync : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AlterDatabase()
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.CreateTable(
                name: "AspNetRoles",
                columns: table => new
                {
                    Id = table.Column<string>(type: "varchar(255)", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    Name = table.Column<string>(type: "varchar(256)", maxLength: 256, nullable: true)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    NormalizedName = table.Column<string>(type: "varchar(256)", maxLength: 256, nullable: true)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    ConcurrencyStamp = table.Column<string>(type: "longtext", nullable: true)
                        .Annotation("MySql:CharSet", "utf8mb4")
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_AspNetRoles", x => x.Id);
                })
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.CreateTable(
                name: "AspNetUsers",
                columns: table => new
                {
                    Id = table.Column<string>(type: "varchar(255)", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    UserName = table.Column<string>(type: "varchar(256)", maxLength: 256, nullable: true)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    NormalizedUserName = table.Column<string>(type: "varchar(256)", maxLength: 256, nullable: true)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    Email = table.Column<string>(type: "varchar(256)", maxLength: 256, nullable: true)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    NormalizedEmail = table.Column<string>(type: "varchar(256)", maxLength: 256, nullable: true)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    EmailConfirmed = table.Column<bool>(type: "tinyint(1)", nullable: false),
                    PasswordHash = table.Column<string>(type: "longtext", nullable: true)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    SecurityStamp = table.Column<string>(type: "longtext", nullable: true)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    ConcurrencyStamp = table.Column<string>(type: "longtext", nullable: true)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    PhoneNumber = table.Column<string>(type: "longtext", nullable: true)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    PhoneNumberConfirmed = table.Column<bool>(type: "tinyint(1)", nullable: false),
                    TwoFactorEnabled = table.Column<bool>(type: "tinyint(1)", nullable: false),
                    LockoutEnd = table.Column<DateTimeOffset>(type: "datetime(6)", nullable: true),
                    LockoutEnabled = table.Column<bool>(type: "tinyint(1)", nullable: false),
                    AccessFailedCount = table.Column<int>(type: "int", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_AspNetUsers", x => x.Id);
                })
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.CreateTable(
                name: "deceaseddetails",
                columns: table => new
                {
                    DeceasedDetailsId = table.Column<int>(type: "int(11)", nullable: false)
                        .Annotation("MySql:ValueGenerationStrategy", MySqlValueGenerationStrategy.IdentityColumn),
                    DeceasedStatusId = table.Column<int>(type: "int(11)", nullable: false),
                    ContactDetailsId = table.Column<int>(type: "int(11)", nullable: false),
                    NoteId = table.Column<int>(type: "int(11)", nullable: false),
                    FirstName = table.Column<string>(type: "longtext", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    LastName = table.Column<string>(type: "longtext", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    Initial = table.Column<string>(type: "longtext", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    DateBuried = table.Column<DateTime>(type: "datetime(6)", maxLength: 6, nullable: false),
                    DoB = table.Column<DateTime>(type: "datetime(6)", maxLength: 6, nullable: false),
                    DoD = table.Column<DateTime>(type: "datetime(6)", maxLength: 6, nullable: false),
                    CreatedDate = table.Column<DateTime>(type: "datetime(6)", maxLength: 6, nullable: false),
                    CreatedBy = table.Column<int>(type: "int(11)", nullable: false),
                    ModifiedDate = table.Column<DateTime>(type: "datetime(6)", maxLength: 6, nullable: false),
                    ModifiedBy = table.Column<int>(type: "int(11)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PRIMARY", x => x.DeceasedDetailsId);
                })
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.CreateTable(
                name: "deceasedstatus",
                columns: table => new
                {
                    DeceasedStatusId = table.Column<int>(type: "int(11)", nullable: false)
                        .Annotation("MySql:ValueGenerationStrategy", MySqlValueGenerationStrategy.IdentityColumn),
                    DeceasedStatusConstant = table.Column<string>(type: "longtext", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    CreatedDate = table.Column<DateTime>(type: "datetime(6)", maxLength: 6, nullable: false),
                    CreatedBy = table.Column<int>(type: "int(11)", nullable: false),
                    ModifiedDate = table.Column<DateTime>(type: "datetime(6)", maxLength: 6, nullable: false),
                    ModifiedBy = table.Column<int>(type: "int(11)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PRIMARY", x => x.DeceasedStatusId);
                })
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.CreateTable(
                name: "maintenancestatus",
                columns: table => new
                {
                    MaintenanceStatusId = table.Column<int>(type: "int(11)", nullable: false)
                        .Annotation("MySql:ValueGenerationStrategy", MySqlValueGenerationStrategy.IdentityColumn),
                    MaintenanceStatusConstant = table.Column<string>(type: "longtext", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    CreatedDate = table.Column<DateTime>(type: "datetime(6)", maxLength: 6, nullable: false),
                    CreatedBy = table.Column<int>(type: "int(11)", nullable: false),
                    ModifiedDate = table.Column<DateTime>(type: "datetime(6)", maxLength: 6, nullable: false),
                    ModifiedBy = table.Column<int>(type: "int(11)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PRIMARY", x => x.MaintenanceStatusId);
                })
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.CreateTable(
                name: "paymentstatus",
                columns: table => new
                {
                    PaymentStatusId = table.Column<int>(type: "int(11)", nullable: false)
                        .Annotation("MySql:ValueGenerationStrategy", MySqlValueGenerationStrategy.IdentityColumn),
                    PaymentStatusConstant = table.Column<string>(type: "longtext", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    CreatedDate = table.Column<DateTime>(type: "datetime(6)", maxLength: 6, nullable: false),
                    CreatedBy = table.Column<int>(type: "int(11)", nullable: false),
                    ModifiedDate = table.Column<DateTime>(type: "datetime(6)", maxLength: 6, nullable: false),
                    ModifiedBy = table.Column<int>(type: "int(11)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PRIMARY", x => x.PaymentStatusId);
                })
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.CreateTable(
                name: "section",
                columns: table => new
                {
                    SectionId = table.Column<int>(type: "int(11)", nullable: false)
                        .Annotation("MySql:ValueGenerationStrategy", MySqlValueGenerationStrategy.IdentityColumn),
                    SectionConstant = table.Column<string>(type: "longtext", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    CreatedDate = table.Column<DateTime>(type: "datetime(6)", maxLength: 6, nullable: false),
                    CreatedBy = table.Column<int>(type: "int(11)", nullable: false),
                    ModifiedDate = table.Column<DateTime>(type: "datetime(6)", maxLength: 6, nullable: false),
                    ModifiedBy = table.Column<int>(type: "int(11)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PRIMARY", x => x.SectionId);
                })
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.CreateTable(
                name: "user",
                columns: table => new
                {
                    UserId = table.Column<int>(type: "int(11)", nullable: false)
                        .Annotation("MySql:ValueGenerationStrategy", MySqlValueGenerationStrategy.IdentityColumn),
                    FirstName = table.Column<string>(type: "longtext", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    LastName = table.Column<string>(type: "longtext", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    Username = table.Column<string>(type: "longtext", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    Password = table.Column<string>(type: "longtext", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    LastLogin = table.Column<DateTime>(type: "datetime(6)", maxLength: 6, nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PRIMARY", x => x.UserId);
                })
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.CreateTable(
                name: "AspNetRoleClaims",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("MySql:ValueGenerationStrategy", MySqlValueGenerationStrategy.IdentityColumn),
                    RoleId = table.Column<string>(type: "varchar(255)", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    ClaimType = table.Column<string>(type: "longtext", nullable: true)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    ClaimValue = table.Column<string>(type: "longtext", nullable: true)
                        .Annotation("MySql:CharSet", "utf8mb4")
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_AspNetRoleClaims", x => x.Id);
                    table.ForeignKey(
                        name: "FK_AspNetRoleClaims_AspNetRoles_RoleId",
                        column: x => x.RoleId,
                        principalTable: "AspNetRoles",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                })
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.CreateTable(
                name: "AspNetUserClaims",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("MySql:ValueGenerationStrategy", MySqlValueGenerationStrategy.IdentityColumn),
                    UserId = table.Column<string>(type: "varchar(255)", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    ClaimType = table.Column<string>(type: "longtext", nullable: true)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    ClaimValue = table.Column<string>(type: "longtext", nullable: true)
                        .Annotation("MySql:CharSet", "utf8mb4")
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_AspNetUserClaims", x => x.Id);
                    table.ForeignKey(
                        name: "FK_AspNetUserClaims_AspNetUsers_UserId",
                        column: x => x.UserId,
                        principalTable: "AspNetUsers",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                })
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.CreateTable(
                name: "AspNetUserLogins",
                columns: table => new
                {
                    LoginProvider = table.Column<string>(type: "varchar(128)", maxLength: 128, nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    ProviderKey = table.Column<string>(type: "varchar(128)", maxLength: 128, nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    ProviderDisplayName = table.Column<string>(type: "longtext", nullable: true)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    UserId = table.Column<string>(type: "varchar(255)", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4")
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_AspNetUserLogins", x => new { x.LoginProvider, x.ProviderKey });
                    table.ForeignKey(
                        name: "FK_AspNetUserLogins_AspNetUsers_UserId",
                        column: x => x.UserId,
                        principalTable: "AspNetUsers",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                })
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.CreateTable(
                name: "AspNetUserRoles",
                columns: table => new
                {
                    UserId = table.Column<string>(type: "varchar(255)", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    RoleId = table.Column<string>(type: "varchar(255)", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4")
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_AspNetUserRoles", x => new { x.UserId, x.RoleId });
                    table.ForeignKey(
                        name: "FK_AspNetUserRoles_AspNetRoles_RoleId",
                        column: x => x.RoleId,
                        principalTable: "AspNetRoles",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                    table.ForeignKey(
                        name: "FK_AspNetUserRoles_AspNetUsers_UserId",
                        column: x => x.UserId,
                        principalTable: "AspNetUsers",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                })
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.CreateTable(
                name: "AspNetUserTokens",
                columns: table => new
                {
                    UserId = table.Column<string>(type: "varchar(255)", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    LoginProvider = table.Column<string>(type: "varchar(128)", maxLength: 128, nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    Name = table.Column<string>(type: "varchar(128)", maxLength: 128, nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    Value = table.Column<string>(type: "longtext", nullable: true)
                        .Annotation("MySql:CharSet", "utf8mb4")
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_AspNetUserTokens", x => new { x.UserId, x.LoginProvider, x.Name });
                    table.ForeignKey(
                        name: "FK_AspNetUserTokens_AspNetUsers_UserId",
                        column: x => x.UserId,
                        principalTable: "AspNetUsers",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                })
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.CreateTable(
                name: "contactdetails",
                columns: table => new
                {
                    ContactDetailsId = table.Column<int>(type: "int(11)", nullable: false)
                        .Annotation("MySql:ValueGenerationStrategy", MySqlValueGenerationStrategy.IdentityColumn),
                    PlotId = table.Column<int>(type: "int(11)", nullable: false),
                    DeceasedDetailsId = table.Column<int>(type: "int(11)", nullable: false),
                    NoteId = table.Column<int>(type: "int(11)", nullable: false),
                    FirstName = table.Column<string>(type: "longtext", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    LastName = table.Column<string>(type: "longtext", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    PhoneNumber = table.Column<string>(type: "longtext", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    Address = table.Column<string>(type: "longtext", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    Email = table.Column<string>(type: "longtext", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    DeceasedDetailsId1 = table.Column<int>(type: "int(11)", nullable: false),
                    CreatedDate = table.Column<DateTime>(type: "datetime(6)", maxLength: 6, nullable: false),
                    CreatedBy = table.Column<int>(type: "int(11)", nullable: false),
                    ModifiedDate = table.Column<DateTime>(type: "datetime(6)", maxLength: 6, nullable: false),
                    ModifiedBy = table.Column<int>(type: "int(11)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PRIMARY", x => x.ContactDetailsId);
                    table.ForeignKey(
                        name: "FK_ContactDetails_DeceasedDetails_DeceasedDetailsId1",
                        column: x => x.DeceasedDetailsId1,
                        principalTable: "deceaseddetails",
                        principalColumn: "DeceasedDetailsId",
                        onDelete: ReferentialAction.Cascade);
                })
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.CreateTable(
                name: "plotdetails",
                columns: table => new
                {
                    PlotDetailsId = table.Column<int>(type: "int(11)", nullable: false)
                        .Annotation("MySql:ValueGenerationStrategy", MySqlValueGenerationStrategy.IdentityColumn),
                    PlotId = table.Column<int>(type: "int(11)", nullable: false),
                    SectionId = table.Column<int>(type: "int(11)", nullable: false),
                    MaintenanceStatusId = table.Column<int>(type: "int(11)", nullable: false),
                    ContactDetailsId = table.Column<int>(type: "int(11)", nullable: false),
                    NoteId = table.Column<int>(type: "int(11)", nullable: false),
                    Row = table.Column<string>(type: "longtext", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    Unit = table.Column<string>(type: "longtext", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    Side = table.Column<string>(type: "longtext", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    Niche = table.Column<string>(type: "longtext", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    DeceasedDetailsId = table.Column<int>(type: "int(11)", nullable: true),
                    CreatedDate = table.Column<DateTime>(type: "datetime(6)", maxLength: 6, nullable: false),
                    CreatedBy = table.Column<int>(type: "int(11)", nullable: false),
                    ModifiedDate = table.Column<DateTime>(type: "datetime(6)", maxLength: 6, nullable: false),
                    ModifiedBy = table.Column<int>(type: "int(11)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PRIMARY", x => x.PlotDetailsId);
                    table.ForeignKey(
                        name: "FK_PlotDetails_ContactDetails_ContactDetailsId",
                        column: x => x.ContactDetailsId,
                        principalTable: "contactdetails",
                        principalColumn: "ContactDetailsId",
                        onDelete: ReferentialAction.Cascade);
                    table.ForeignKey(
                        name: "FK_PlotDetails_DeceasedDetails_DeceasedDetailsId",
                        column: x => x.DeceasedDetailsId,
                        principalTable: "deceaseddetails",
                        principalColumn: "DeceasedDetailsId");
                    table.ForeignKey(
                        name: "FK_PlotDetails_MaintenanceStatus_MaintenanceStatusId",
                        column: x => x.MaintenanceStatusId,
                        principalTable: "maintenancestatus",
                        principalColumn: "MaintenanceStatusId",
                        onDelete: ReferentialAction.Cascade);
                    table.ForeignKey(
                        name: "FK_PlotDetails_PlotDetails_PlotId",
                        column: x => x.PlotId,
                        principalTable: "plotdetails",
                        principalColumn: "PlotDetailsId",
                        onDelete: ReferentialAction.Cascade);
                    table.ForeignKey(
                        name: "FK_PlotDetails_Section_SectionId",
                        column: x => x.SectionId,
                        principalTable: "section",
                        principalColumn: "SectionId",
                        onDelete: ReferentialAction.Cascade);
                })
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.CreateTable(
                name: "maintenancedetails",
                columns: table => new
                {
                    MaintId = table.Column<int>(type: "int(11)", nullable: false)
                        .Annotation("MySql:ValueGenerationStrategy", MySqlValueGenerationStrategy.IdentityColumn),
                    Description = table.Column<string>(type: "longtext", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    PlotDetailsId = table.Column<int>(type: "int(11)", nullable: false),
                    MaintenanceStatusId = table.Column<int>(type: "int(11)", nullable: false),
                    CreatedDate = table.Column<DateTime>(type: "datetime(6)", maxLength: 6, nullable: false),
                    CreatedBy = table.Column<int>(type: "int(11)", nullable: false),
                    ModifiedDate = table.Column<DateTime>(type: "datetime(6)", maxLength: 6, nullable: false),
                    ModifiedBy = table.Column<int>(type: "int(11)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PRIMARY", x => x.MaintId);
                    table.ForeignKey(
                        name: "FK_MaintenanceDetails_MaintenanceStatus_MaintenanceStatusId",
                        column: x => x.MaintenanceStatusId,
                        principalTable: "maintenancestatus",
                        principalColumn: "MaintenanceStatusId",
                        onDelete: ReferentialAction.Cascade);
                    table.ForeignKey(
                        name: "FK_MaintenanceDetails_PlotDetails_PlotDetailsId",
                        column: x => x.PlotDetailsId,
                        principalTable: "plotdetails",
                        principalColumn: "PlotDetailsId",
                        onDelete: ReferentialAction.Cascade);
                })
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.CreateTable(
                name: "paymentdetails",
                columns: table => new
                {
                    PaymentDetailsID = table.Column<int>(type: "int(11)", nullable: false)
                        .Annotation("MySql:ValueGenerationStrategy", MySqlValueGenerationStrategy.IdentityColumn),
                    PlotId = table.Column<int>(type: "int(11)", nullable: false),
                    DeceasedDetailsId = table.Column<int>(type: "int(11)", nullable: false),
                    PaymentStatusId = table.Column<int>(type: "int(11)", nullable: false),
                    ContactDetailsId = table.Column<int>(type: "int(11)", nullable: false),
                    NoteId = table.Column<int>(type: "int(11)", nullable: false),
                    BalancePaid = table.Column<decimal>(type: "decimal(65,30)", nullable: false),
                    BalanceDue = table.Column<decimal>(type: "decimal(65,30)", nullable: false),
                    CreatedDate = table.Column<DateTime>(type: "datetime(6)", maxLength: 6, nullable: false),
                    CreatedBy = table.Column<int>(type: "int(11)", nullable: false),
                    ModifiedDate = table.Column<DateTime>(type: "datetime(6)", maxLength: 6, nullable: false),
                    ModifiedBy = table.Column<int>(type: "int(11)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PRIMARY", x => x.PaymentDetailsID);
                    table.ForeignKey(
                        name: "FK_PaymentDetails_ContactDetails_ContactDetailsId",
                        column: x => x.ContactDetailsId,
                        principalTable: "contactdetails",
                        principalColumn: "ContactDetailsId",
                        onDelete: ReferentialAction.Cascade);
                    table.ForeignKey(
                        name: "FK_PaymentDetails_DeceasedDetails_DeceasedDetailsId",
                        column: x => x.DeceasedDetailsId,
                        principalTable: "deceaseddetails",
                        principalColumn: "DeceasedDetailsId",
                        onDelete: ReferentialAction.Cascade);
                    table.ForeignKey(
                        name: "FK_PaymentDetails_PaymentStatus_PaymentStatusId",
                        column: x => x.PaymentStatusId,
                        principalTable: "paymentstatus",
                        principalColumn: "PaymentStatusId",
                        onDelete: ReferentialAction.Cascade);
                    table.ForeignKey(
                        name: "FK_PaymentDetails_PlotDetails_PlotId",
                        column: x => x.PlotId,
                        principalTable: "plotdetails",
                        principalColumn: "PlotDetailsId",
                        onDelete: ReferentialAction.Cascade);
                })
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.CreateTable(
                name: "notes",
                columns: table => new
                {
                    NoteId = table.Column<int>(type: "int(11)", nullable: false)
                        .Annotation("MySql:ValueGenerationStrategy", MySqlValueGenerationStrategy.IdentityColumn),
                    UserId = table.Column<int>(type: "int(11)", nullable: false),
                    Content = table.Column<string>(type: "longtext", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    CreatedDate = table.Column<DateTime>(type: "datetime(6)", maxLength: 6, nullable: false),
                    CreatedBy = table.Column<int>(type: "int(11)", nullable: false),
                    ModifiedDate = table.Column<DateTime>(type: "datetime(6)", maxLength: 6, nullable: false),
                    ModifiedBy = table.Column<int>(type: "int(11)", nullable: false),
                    ContactDetailsId = table.Column<int>(type: "int(11)", nullable: true),
                    DeceasedDetailsId = table.Column<int>(type: "int(11)", nullable: true),
                    MaintenanceDetailsMaintId = table.Column<int>(type: "int(11)", nullable: true),
                    PlotDetailsId = table.Column<int>(type: "int(11)", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PRIMARY", x => x.NoteId);
                    table.ForeignKey(
                        name: "FK_Notes_ContactDetails_ContactDetailsId",
                        column: x => x.ContactDetailsId,
                        principalTable: "contactdetails",
                        principalColumn: "ContactDetailsId");
                    table.ForeignKey(
                        name: "FK_Notes_DeceasedDetails_DeceasedDetailsId",
                        column: x => x.DeceasedDetailsId,
                        principalTable: "deceaseddetails",
                        principalColumn: "DeceasedDetailsId");
                    table.ForeignKey(
                        name: "FK_Notes_MaintenanceDetails_MaintenanceDetailsMaintId",
                        column: x => x.MaintenanceDetailsMaintId,
                        principalTable: "maintenancedetails",
                        principalColumn: "MaintId");
                    table.ForeignKey(
                        name: "FK_Notes_PlotDetails_PlotDetailsId",
                        column: x => x.PlotDetailsId,
                        principalTable: "plotdetails",
                        principalColumn: "PlotDetailsId");
                    table.ForeignKey(
                        name: "FK_Notes_User_UserId",
                        column: x => x.UserId,
                        principalTable: "user",
                        principalColumn: "UserId",
                        onDelete: ReferentialAction.Cascade);
                })
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.CreateIndex(
                name: "IX_AspNetRoleClaims_RoleId",
                table: "AspNetRoleClaims",
                column: "RoleId");

            migrationBuilder.CreateIndex(
                name: "RoleNameIndex",
                table: "AspNetRoles",
                column: "NormalizedName",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_AspNetUserClaims_UserId",
                table: "AspNetUserClaims",
                column: "UserId");

            migrationBuilder.CreateIndex(
                name: "IX_AspNetUserLogins_UserId",
                table: "AspNetUserLogins",
                column: "UserId");

            migrationBuilder.CreateIndex(
                name: "IX_AspNetUserRoles_RoleId",
                table: "AspNetUserRoles",
                column: "RoleId");

            migrationBuilder.CreateIndex(
                name: "EmailIndex",
                table: "AspNetUsers",
                column: "NormalizedEmail");

            migrationBuilder.CreateIndex(
                name: "UserNameIndex",
                table: "AspNetUsers",
                column: "NormalizedUserName",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_ContactDetails_DeceasedDetailsId1",
                table: "contactdetails",
                column: "DeceasedDetailsId1");

            migrationBuilder.CreateIndex(
                name: "IX_MaintenanceDetails_MaintenanceStatusId",
                table: "maintenancedetails",
                column: "MaintenanceStatusId");

            migrationBuilder.CreateIndex(
                name: "IX_MaintenanceDetails_PlotDetailsId",
                table: "maintenancedetails",
                column: "PlotDetailsId");

            migrationBuilder.CreateIndex(
                name: "IX_Notes_ContactDetailsId",
                table: "notes",
                column: "ContactDetailsId");

            migrationBuilder.CreateIndex(
                name: "IX_Notes_DeceasedDetailsId",
                table: "notes",
                column: "DeceasedDetailsId");

            migrationBuilder.CreateIndex(
                name: "IX_Notes_MaintenanceDetailsMaintId",
                table: "notes",
                column: "MaintenanceDetailsMaintId");

            migrationBuilder.CreateIndex(
                name: "IX_Notes_PlotDetailsId",
                table: "notes",
                column: "PlotDetailsId");

            migrationBuilder.CreateIndex(
                name: "IX_Notes_UserId",
                table: "notes",
                column: "UserId");

            migrationBuilder.CreateIndex(
                name: "IX_PaymentDetails_ContactDetailsId",
                table: "paymentdetails",
                column: "ContactDetailsId");

            migrationBuilder.CreateIndex(
                name: "IX_PaymentDetails_DeceasedDetailsId",
                table: "paymentdetails",
                column: "DeceasedDetailsId");

            migrationBuilder.CreateIndex(
                name: "IX_PaymentDetails_PaymentStatusId",
                table: "paymentdetails",
                column: "PaymentStatusId");

            migrationBuilder.CreateIndex(
                name: "IX_PaymentDetails_PlotId",
                table: "paymentdetails",
                column: "PlotId");

            migrationBuilder.CreateIndex(
                name: "IX_PlotDetails_ContactDetailsId",
                table: "plotdetails",
                column: "ContactDetailsId",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_PlotDetails_DeceasedDetailsId",
                table: "plotdetails",
                column: "DeceasedDetailsId");

            migrationBuilder.CreateIndex(
                name: "IX_PlotDetails_MaintenanceStatusId",
                table: "plotdetails",
                column: "MaintenanceStatusId");

            migrationBuilder.CreateIndex(
                name: "IX_PlotDetails_PlotId",
                table: "plotdetails",
                column: "PlotId");

            migrationBuilder.CreateIndex(
                name: "IX_PlotDetails_SectionId",
                table: "plotdetails",
                column: "SectionId");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "AspNetRoleClaims");

            migrationBuilder.DropTable(
                name: "AspNetUserClaims");

            migrationBuilder.DropTable(
                name: "AspNetUserLogins");

            migrationBuilder.DropTable(
                name: "AspNetUserRoles");

            migrationBuilder.DropTable(
                name: "AspNetUserTokens");

            migrationBuilder.DropTable(
                name: "deceasedstatus");

            migrationBuilder.DropTable(
                name: "notes");

            migrationBuilder.DropTable(
                name: "paymentdetails");

            migrationBuilder.DropTable(
                name: "AspNetRoles");

            migrationBuilder.DropTable(
                name: "AspNetUsers");

            migrationBuilder.DropTable(
                name: "maintenancedetails");

            migrationBuilder.DropTable(
                name: "user");

            migrationBuilder.DropTable(
                name: "paymentstatus");

            migrationBuilder.DropTable(
                name: "plotdetails");

            migrationBuilder.DropTable(
                name: "contactdetails");

            migrationBuilder.DropTable(
                name: "maintenancestatus");

            migrationBuilder.DropTable(
                name: "section");

            migrationBuilder.DropTable(
                name: "deceaseddetails");
        }
    }
}
