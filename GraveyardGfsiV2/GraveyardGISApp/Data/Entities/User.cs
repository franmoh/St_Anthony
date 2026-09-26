using System;
using System.Collections.Generic;

namespace GraveyardGISApp.Data.Entities;

public partial class User
{
    public int UserId { get; set; }

    public string FirstName { get; set; } = null!;

    public string LastName { get; set; } = null!;

    public string Username { get; set; } = null!;

    public string Password { get; set; } = null!;

    public DateTime LastLogin { get; set; }

    public virtual ICollection<Note> Notes { get; set; } = new List<Note>();
}
