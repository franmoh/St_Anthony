using System.ComponentModel.DataAnnotations;

namespace GraveyardGFSI.Data.Entities
{
    public class User
    {
        [Key]
        public int UserId { get; set; }
        public string FirstName { get; set; } = string.Empty;
        public string LastName { get; set; } = string.Empty;
        public string Username { get; set; } = string.Empty;
        public string Password { get; set; } = string.Empty;
        public DateTime LastLogin { get; set; }

        // 
        public ICollection<Note> Notes = new List<Note>();
        // public Note? Note { get; set; }

        public User() { }

        public User(int userId, string firstName, string lastName, string username, string password, DateTime lastLogin)
        {
            this.UserId = userId;
            this.FirstName = firstName;
            this.LastName = lastName;
            this.Username = username;
            this.Password = password;
            this.LastLogin = lastLogin;

        }
    }
}
