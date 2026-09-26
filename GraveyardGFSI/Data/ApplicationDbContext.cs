using GraveyardGFSI.Data.Entities;
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;

namespace GraveyardGFSI.Data
{
    public class ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) : IdentityDbContext<ApplicationUser>(options)
    {
        // Entity sets to map to DB.
        
        public DbSet<ContactDetails> ContactDetails { get; set; }
        public DbSet<DeceasedDetails> DeceasedDetails { get; set; }
        public DbSet<DeceasedStatus> DeceasedStatus { get; set; }
        public DbSet<MaintenanceDetails> MaintenanceDetails { get; set; }
        public DbSet<MaintenanceStatus> MaintenanceStatus { get; set; }
        public DbSet<Note> Notes { get; set; }
        public DbSet<PaymentDetails> PaymentDetails { get; set; }
        public DbSet<PaymentStatus> PaymentStatus { get; set; }
        public DbSet<PlotDetails> PlotDetails { get; set; }
        public DbSet<Section> Section { get; set; }
        
        // public DbSet<User> Users { get; set; }
    }

}
