(function(){
  function parseBool(v){
    if (typeof v === "boolean") return v;
    if (typeof v === "string") return v.toLowerCase() === "true";
    return !!v;
  }
  function parseNum(v){
    var n = parseFloat(v);
    return isNaN(n) ? null : n;
  }
  function op(left, operator, right){
    switch(operator){
      case ">=": return left !== null && left >= right;
      case ">":  return left !== null && left > right;
      case "==": return left === right;
      case "<=": return left !== null && left <= right;
      case "<":  return left !== null && left < right;
      case "!=": return left !== right;
    }
    return false;
  }
  function meetsCriteria(state, criteria){
    for (var i=0;i<criteria.length;i++){
      var c = criteria[i];
      if (c.field){
        if (!op(state[c.field], c.op, c.value)) return false;
      } else if (c.any_of){
        var anyOk = false;
        for (var j=0;j<c.any_of.length;j++){
          var x = c.any_of[j];
          if (op(state[x.field], x.op, x.value)) { anyOk = true; break; }
        }
        if (!anyOk) return false;
      } else if (c.all_of){
        var allOk = true;
        for (var k=0;k<c.all_of.length;k++){
          var y = c.all_of[k];
          if (!op(state[y.field], y.op, y.value)) { allOk = false; break; }
        }
        if (!allOk) return false;
      } else {
        return false;
      }
    }
    return true;
  }

  async function init(el){
    var d = el.dataset;
    var rulesUrl = d.rulesUrl;
    if (!rulesUrl) {
      el.innerHTML = "<em>Rules URL missing.</em>";
      return;
    }
    var res = await fetch(rulesUrl, {cache:"no-store"});
    var rules = await res.json();

    // Build internal state from shortcode data-attrs (same names as Python mapping targets)
    var state = {
      credits_used_pct: parseNum(d.creditsUsedPct),
      peak_bookings_14d: parseNum(d.peakBookings14d),
      waitlist_events_30d: parseNum(d.waitlistEvents30d),
      household_members: parseNum(d.householdMembers),
      has_annual: parseBool(d.hasAnnual),
      recent_renewals_count: parseNum(d.recentRenewalsCount)
    };
    var memberId = d.memberId || "unknown_member";
    var currentTier = d.currentTier || "Explorer";

    // Match trigger
    var matched = null;
    for (var i=0;i<rules.triggers.length;i++){
      var trig = rules.triggers[i];
      var fromTier = trig.from_tier || "Any";
      if (fromTier !== "Any" && fromTier !== currentTier) continue;
      if (meetsCriteria(state, trig.criteria || [])) { matched = trig; break; }
    }

    if (!matched){
      el.innerHTML = '<div class="nxs-foot">No upgrade suggestion right now.</div>';
      return;
    }

    var reward = Object.assign({}, matched.reward || {});
    var msg = matched.message || {};
    // interpolate message with reward keys
    function fmt(str){
      return str.replace(/\{(\w+)\}/g, function(_, k){
        return (k in reward) ? reward[k] : "";
      });
    }
    var title = msg.title || "Upgrade available";
    var body = fmt(msg.body || "");

    var upgradeUrl = d.upgradeUrl || "#";
    var keepUrl = d.keepUrl || "#";
    var compareUrl = d.compareUrl || "#";

    el.innerHTML = ''
      + '<span class="nxs-badge">Loyalty upgrade</span>'
      + '<h3>'+ title +'</h3>'
      + '<p>'+ body +'</p>'
      + '<div class="nxs-pills">'
      +   '<span class="pill">Credits used: '+ Math.round((state.credits_used_pct||0)*100) +'%</span>'
      +   '<span class="pill">Peak bookings (14d): '+ (state.peak_bookings_14d||0) +'</span>'
      +   '<span class="pill">Household: '+ (state.household_members||1) +'</span>'
      + '</div>'
      + '<div class="nxs-cta">'
      +   '<a class="btn btn-primary" href="'+ upgradeUrl +'">'+ (msg.cta_primary || "Upgrade") +'</a>'
      +   '<a class="btn btn-secondary" href="'+ keepUrl +'">'+ (msg.cta_secondary || "Not now") +'</a>'
      +   '<a class="btn btn-secondary" href="'+ compareUrl +'">'+ (msg.cta_tertiary || "Compare plans") +'</a>'
      + '</div>'
      + '<div class="nxs-foot">From '+ currentTier +' → '+ matched.to_tier +'</div>';
  }

  document.addEventListener("DOMContentLoaded", function(){
    document.querySelectorAll(".nxs-upgrade").forEach(init);
  });
})();