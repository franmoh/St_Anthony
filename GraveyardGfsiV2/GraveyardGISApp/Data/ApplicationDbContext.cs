using GraveyardGISApp.Data.Entities;
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;

namespace GraveyardGISApp.Data
{
    public class ApplicationDbContext : IdentityDbContext
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
            : base(options)
        {
            Console.WriteLine($"*** EF Connected To Database: {Database.GetDbConnection().Database} ***");
        }
        // Migrations throws a fit if this stuff is included.

        public virtual DbSet<Contactdetail> Contactdetails { get; set; }

        public virtual DbSet<Deceaseddetail> Deceaseddetails { get; set; }

        public virtual DbSet<Deceasedcontactmapping> Deceasedcontactmappings { get; set; }

        public virtual DbSet<Deceasedstatus> Deceasedstatuses { get; set; }

        // public virtual DbSet<Efmigrationshistory> Efmigrationshistories { get; set; }

        public virtual DbSet<Maintenancedetail> Maintenancedetails { get; set; }

        public virtual DbSet<Maintenancestatus> Maintenancestatuses { get; set; }

        public virtual DbSet<Note> Notes { get; set; }

        public virtual DbSet<Paymentdetail> Paymentdetails { get; set; }

        public virtual DbSet<Paymentstatus> Paymentstatuses { get; set; }

        public virtual DbSet<Plotcontactmapping> Plotcontactmappings { get; set; }

        public virtual DbSet<Plotdetail> Plotdetails { get; set; }

        public virtual DbSet<Section> Sections { get; set; }

        public virtual DbSet<User> User { get; set; }
        
        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            modelBuilder.Entity<Contactdetail>(entity =>
            {
                entity.HasKey(e => e.ContactDetailsId).HasName("PRIMARY");
                entity.ToTable("ContactDetails");
                entity.Property(e => e.ContactDetailsId).HasColumnType("int(11)").HasColumnName("ContactDetailsID");
                entity.Property(e => e.NoteId).HasColumnType("int(11)").HasColumnName("NoteID");
                entity.Property(e => e.CreatedBy).HasColumnType("int(11)");
                entity.Property(e => e.ModifiedBy).HasColumnType("int(11)");
            });

            modelBuilder.Entity<Deceaseddetail>(entity =>
            {
                entity.HasKey(e => e.DeceasedDetailsId).HasName("PRIMARY");

                entity.ToTable("DeceasedDetails");

                entity.Property(e => e.DeceasedDetailsId).HasColumnType("int(11)").HasColumnName("DeceasedDetailsID");
                entity.Property(e => e.PlotId).HasColumnType("int(11)").HasColumnName("PlotID");
                entity.Property(e => e.ZoneId).HasColumnType("int(11)").HasColumnName("ZoneID");
                entity.Property(e => e.DeceasedStatusId).HasColumnType("int(11)").HasColumnName("DeceasedStatusID");
                entity.Property(e => e.NoteId).HasColumnType("int(11)").HasColumnName("NoteID");
                entity.Property(e => e.DOBYear).HasColumnName("DOBYear");
                entity.Property(e => e.DOBMonth).HasColumnName("DOBMonth");
                entity.Property(e => e.DOBDay).HasColumnName("DOBDay");
                entity.Property(e => e.DODYear).HasColumnName("DODYear");
                entity.Property(e => e.DODMonth).HasColumnName("DODMonth");
                entity.Property(e => e.DODDay).HasColumnName("DODDay");
                entity.Property(e => e.CreatedBy).HasColumnType("int(11)");
                entity.Property(e => e.ModifiedBy).HasColumnType("int(11)");
            });

            modelBuilder.Entity<Deceasedcontactmapping>(entity =>
            {
                entity.HasKey(e => e.DeceasedContactMappingId).HasName("PRIMARY");
                entity.ToTable("DeceasedContactMapping");
                entity.Property(e => e.DeceasedContactMappingId).HasColumnType("int(11)").HasColumnName("DeceasedContactMappingID");
                entity.Property(e => e.DeceasedDetailsId).HasColumnType("int(11)").HasColumnName("DeceasedDetailsID");
                entity.Property(e => e.ContactDetailsId).HasColumnType("int(11)").HasColumnName("ContactDetailsID");
                entity.Property(e => e.CreatedBy).HasColumnType("int(11)");
                entity.Property(e => e.ModifiedBy).HasColumnType("int(11)");
            });

            modelBuilder.Entity<Plotcontactmapping>(entity =>
            {
                entity.HasKey(e => e.PlotContactMappingId).HasName("PRIMARY");
                entity.ToTable("PlotContactMapping");
                entity.Property(e => e.PlotContactMappingId).HasColumnType("int(11)").HasColumnName("PlotContactMappingID");
                entity.Property(e => e.PlotDetailsId).HasColumnType("int(11)").HasColumnName("PlotDetailsID");
                entity.Property(e => e.ContactDetailsId).HasColumnType("int(11)").HasColumnName("ContactDetailsID");
                entity.Property(e => e.CreatedBy).HasColumnType("int(11)");
                entity.Property(e => e.ModifiedBy).HasColumnType("int(11)");
            });

            modelBuilder.Entity<Deceasedstatus>(entity =>
            {
                entity.HasKey(e => e.DeceasedStatusId).HasName("PRIMARY");

                entity.ToTable("deceasedstatus");

                entity.Property(e => e.DeceasedStatusId).HasColumnType("int(11)");
                entity.Property(e => e.CreatedBy).HasColumnType("int(11)");
                entity.Property(e => e.CreatedDate).HasMaxLength(6);
                entity.Property(e => e.ModifiedBy).HasColumnType("int(11)");
                entity.Property(e => e.ModifiedDate).HasMaxLength(6);
            });

            modelBuilder.Entity<Maintenancedetail>(entity =>
            {
                entity.HasKey(e => e.MaintId).HasName("PRIMARY");

                entity.ToTable("maintenancedetails");

                entity.HasIndex(e => e.MaintenanceStatusId, "IX_MaintenanceDetails_MaintenanceStatusId");

                entity.HasIndex(e => e.PlotDetailsId, "IX_MaintenanceDetails_PlotDetailsId");

                entity.Property(e => e.MaintId).HasColumnType("int(11)");
                entity.Property(e => e.CreatedBy).HasColumnType("int(11)");
                entity.Property(e => e.CreatedDate).HasMaxLength(6);
                entity.Property(e => e.MaintenanceStatusId).HasColumnType("int(11)");
                entity.Property(e => e.ModifiedBy).HasColumnType("int(11)");
                entity.Property(e => e.ModifiedDate).HasMaxLength(6);
                entity.Property(e => e.PlotDetailsId).HasColumnType("int(11)");

                entity.HasOne(d => d.MaintenanceStatus).WithMany(p => p.Maintenancedetails)
                    .HasForeignKey(d => d.MaintenanceStatusId)
                    .HasConstraintName("FK_MaintenanceDetails_MaintenanceStatus_MaintenanceStatusId");

                entity.HasOne(d => d.PlotDetails).WithMany(p => p.Maintenancedetails)
                    .HasForeignKey(d => d.PlotDetailsId)
                    .HasConstraintName("FK_MaintenanceDetails_PlotDetails_PlotDetailsId");
            });

            modelBuilder.Entity<Maintenancestatus>(entity =>
            {
                entity.HasKey(e => e.MaintenanceStatusId).HasName("PRIMARY");

                entity.ToTable("maintenancestatus");

                entity.Property(e => e.MaintenanceStatusId).HasColumnType("int(11)");
                entity.Property(e => e.CreatedBy).HasColumnType("int(11)");
                entity.Property(e => e.CreatedDate).HasMaxLength(6);
                entity.Property(e => e.ModifiedBy).HasColumnType("int(11)");
                entity.Property(e => e.ModifiedDate).HasMaxLength(6);
            });

            modelBuilder.Entity<Note>(entity =>
            {
                entity.HasKey(e => e.NoteId).HasName("PRIMARY");

                entity.ToTable("notes");

                entity.HasIndex(e => e.ContactDetailsId, "IX_Notes_ContactDetailsId");

                entity.HasIndex(e => e.DeceasedDetailsId, "IX_Notes_DeceasedDetailsId");

                entity.HasIndex(e => e.MaintenanceDetailsMaintId, "IX_Notes_MaintenanceDetailsMaintId");

                entity.HasIndex(e => e.PlotDetailsId, "IX_Notes_PlotDetailsId");

                entity.HasIndex(e => e.UserId, "IX_Notes_UserId");

                entity.Property(e => e.NoteId).HasColumnType("int(11)");
                entity.Property(e => e.ContactDetailsId).HasColumnType("int(11)");
                entity.Property(e => e.CreatedBy).HasColumnType("int(11)");
                entity.Property(e => e.CreatedDate).HasMaxLength(6);
                entity.Property(e => e.DeceasedDetailsId).HasColumnType("int(11)");
                entity.Property(e => e.MaintenanceDetailsMaintId).HasColumnType("int(11)");
                entity.Property(e => e.ModifiedBy).HasColumnType("int(11)");
                entity.Property(e => e.ModifiedDate).HasMaxLength(6);
                entity.Property(e => e.PlotDetailsId).HasColumnType("int(11)");
                entity.Property(e => e.UserId).HasColumnType("int(11)");

                entity.HasOne(d => d.ContactDetails).WithMany()
                    .HasForeignKey(d => d.ContactDetailsId)
                    .HasConstraintName("FK_Notes_ContactDetails_ContactDetailsId");

                entity.HasOne(d => d.DeceasedDetails).WithMany(p => p.Notes)
                    .HasForeignKey(d => d.DeceasedDetailsId)
                    .HasConstraintName("FK_Notes_DeceasedDetails_DeceasedDetailsId");

                entity.HasOne(d => d.MaintenanceDetailsMaint).WithMany(p => p.Notes)
                    .HasForeignKey(d => d.MaintenanceDetailsMaintId)
                    .HasConstraintName("FK_Notes_MaintenanceDetails_MaintenanceDetailsMaintId");

                entity.HasOne(d => d.PlotDetails).WithMany(p => p.Notes)
                    .HasForeignKey(d => d.PlotDetailsId)
                    .HasConstraintName("FK_Notes_PlotDetails_PlotDetailsId");

                entity.HasOne(d => d.User).WithMany(p => p.Notes)
                    .HasForeignKey(d => d.UserId)
                    .HasConstraintName("FK_Notes_User_UserId");
            });

            modelBuilder.Entity<Paymentdetail>(entity =>
            {
                entity.HasKey(e => e.PaymentDetailsId).HasName("PRIMARY");

                entity.ToTable("paymentdetails");

                entity.HasIndex(e => e.ContactDetailsId, "IX_PaymentDetails_ContactDetailsId");

                entity.HasIndex(e => e.DeceasedDetailsId, "IX_PaymentDetails_DeceasedDetailsId");

                entity.HasIndex(e => e.PaymentStatusId, "IX_PaymentDetails_PaymentStatusId");

                entity.HasIndex(e => e.PlotId, "IX_PaymentDetails_PlotId");

                entity.Property(e => e.PaymentDetailsId)
                    .HasColumnType("int(11)")
                    .HasColumnName("PaymentDetailsID");
                entity.Property(e => e.ContactDetailsId).HasColumnType("int(11)");
                entity.Property(e => e.CreatedBy).HasColumnType("int(11)");
                entity.Property(e => e.CreatedDate).HasMaxLength(6);
                entity.Property(e => e.DeceasedDetailsId).HasColumnType("int(11)");
                entity.Property(e => e.ModifiedBy).HasColumnType("int(11)");
                entity.Property(e => e.ModifiedDate).HasMaxLength(6);
                entity.Property(e => e.NoteId).HasColumnType("int(11)");
                entity.Property(e => e.PaymentStatusId).HasColumnType("int(11)");
                entity.Property(e => e.PlotId).HasColumnType("int(11)");

                entity.HasOne(d => d.ContactDetails).WithMany()
                    .HasForeignKey(d => d.ContactDetailsId)
                    .HasConstraintName("FK_PaymentDetails_ContactDetails_ContactDetailsId");

                entity.HasOne(d => d.DeceasedDetails).WithMany(p => p.Paymentdetails)
                    .HasForeignKey(d => d.DeceasedDetailsId)
                    .HasConstraintName("FK_PaymentDetails_DeceasedDetails_DeceasedDetailsId");

                entity.HasOne(d => d.PaymentStatus).WithMany(p => p.Paymentdetails)
                    .HasForeignKey(d => d.PaymentStatusId)
                    .HasConstraintName("FK_PaymentDetails_PaymentStatus_PaymentStatusId");

                entity.HasOne(d => d.Plot).WithMany(p => p.Paymentdetails)
                    .HasForeignKey(d => d.PlotId)
                    .HasConstraintName("FK_PaymentDetails_PlotDetails_PlotId");
            });

            modelBuilder.Entity<Paymentstatus>(entity =>
            {
                entity.HasKey(e => e.PaymentStatusId).HasName("PRIMARY");

                entity.ToTable("paymentstatus");

                entity.Property(e => e.PaymentStatusId).HasColumnType("int(11)");
                entity.Property(e => e.CreatedBy).HasColumnType("int(11)");
                entity.Property(e => e.CreatedDate).HasMaxLength(6);
                entity.Property(e => e.ModifiedBy).HasColumnType("int(11)");
                entity.Property(e => e.ModifiedDate).HasMaxLength(6);
            });

            modelBuilder.Entity<Plotdetail>(entity =>
            {
                entity.HasKey(e => e.PlotDetailsId).HasName("PRIMARY");

                entity.ToTable("plotdetails");

                entity.HasIndex(e => e.MaintenanceStatusId, "IX_PlotDetails_MaintenanceStatusId");

                entity.HasIndex(e => e.PlotId, "IX_PlotDetails_PlotId");

                entity.HasIndex(e => e.SectionId, "IX_PlotDetails_SectionId");

                entity.Property(e => e.PlotDetailsId).HasColumnType("int(11)");
                entity.Property(e => e.CreatedBy).HasColumnType("int(11)");
                entity.Property(e => e.CreatedDate).HasMaxLength(6);
                entity.Property(e => e.MaintenanceStatusId).HasColumnType("int(11)");
                entity.Property(e => e.ModifiedBy).HasColumnType("int(11)");
                entity.Property(e => e.ModifiedDate).HasMaxLength(6);
                entity.Property(e => e.NoteId).HasColumnType("int(11)");
                entity.Property(e => e.PlotId).HasColumnType("int(11)");
                entity.Property(e => e.SectionId).HasColumnType("int(11)");
                entity.Property(e => e.PlotStatus).HasColumnName("PlotStatus");
                entity.Property(e => e.IsAvailable).HasColumnName("IsAvailable");

                entity.HasOne(d => d.MaintenanceStatus).WithMany(p => p.Plotdetails)
                    .HasForeignKey(d => d.MaintenanceStatusId)
                    .HasConstraintName("FK_PlotDetails_MaintenanceStatus_MaintenanceStatusId");

                entity.HasOne(d => d.Plot).WithMany(p => p.InversePlot)
                    .HasForeignKey(d => d.PlotId)
                    .HasConstraintName("FK_PlotDetails_PlotDetails_PlotId");

                entity.HasOne(d => d.Section).WithMany(p => p.Plotdetails)
                    .HasForeignKey(d => d.SectionId)
                    .HasConstraintName("FK_PlotDetails_Section_SectionId");
            });

            modelBuilder.Entity<Section>(entity =>
            {
                entity.HasKey(e => e.SectionId).HasName("PRIMARY");

                entity.ToTable("section");

                entity.Property(e => e.SectionId).HasColumnType("int(11)");
                entity.Property(e => e.CreatedBy).HasColumnType("int(11)");
                entity.Property(e => e.CreatedDate).HasMaxLength(6);
                entity.Property(e => e.ModifiedBy).HasColumnType("int(11)");
                entity.Property(e => e.ModifiedDate).HasMaxLength(6);
            });

            modelBuilder.Entity<User>(entity =>
            {
                entity.HasKey(e => e.UserId).HasName("PRIMARY");

                entity.ToTable("user");

                entity.Property(e => e.UserId).HasColumnType("int(11)");
                entity.Property(e => e.LastLogin).HasMaxLength(6);
            });

            // OnModelCreatingPartial(modelBuilder);
        }
    }
}