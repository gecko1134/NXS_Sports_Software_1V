<?php
/**
 * Plugin Name: NXS Upgrade Prompt
 * Description: Shortcode [nxs_upgrade_prompt] to display a membership upgrade banner using a rules JSON. Lightweight, cache-safe, and theme-agnostic.
 * Version: 1.0.0
 * Author: NXS
 */

if (!defined('ABSPATH')) { exit; }

function nxs_upgrade_prompt_enqueue() {
    wp_register_style('nxs-upgrade-style', plugins_url('assets/nxs-upgrade.css', __FILE__), array(), '1.0.0');
    wp_register_script('nxs-upgrade-script', plugins_url('assets/nxs-upgrade.js', __FILE__), array(), '1.0.0', true);
    wp_enqueue_style('nxs-upgrade-style');
    wp_enqueue_script('nxs-upgrade-script');
}
add_action('wp_enqueue_scripts', 'nxs_upgrade_prompt_enqueue');

/**
 * Shortcode:
 * [nxs_upgrade_prompt rules_url="https://example.com/membership_upgrade_rules.json"
 *     member_id="demo_member_123"
 *     current_tier="Explorer"
 *     credits_used_pct="0.83"
 *     peak_bookings_14d="2"
 *     waitlist_events_30d="1"
 *     household_members="4"
 *     has_annual="false"
 *     recent_renewals_count="3"
 *     upgrade_url="https://portal.nationalsportsdome.com/upgrade?familyplus"
 *     keep_url="https://portal.nationalsportsdome.com/keep-current"
 *     compare_url="https://nationalsportsdome.com/memberships"
 * ]
 */
function nxs_upgrade_prompt_shortcode($atts) {
    $a = shortcode_atts(array(
        'rules_url' => '',
        'member_id' => 'unknown_member',
        'current_tier' => 'Explorer',
        'credits_used_pct' => '',
        'peak_bookings_14d' => '',
        'waitlist_events_30d' => '',
        'household_members' => '',
        'has_annual' => '',
        'recent_renewals_count' => '',
        'upgrade_url' => '#',
        'keep_url' => '#',
        'compare_url' => '#'
    ), $atts);

    // Cast booleans/numbers safely for data-* attributes
    $data_attrs = sprintf(
        'data-rules-url="%s" data-member-id="%s" data-current-tier="%s" data-credits-used-pct="%s" data-peak-bookings-14d="%s" data-waitlist-events-30d="%s" data-household-members="%s" data-has-annual="%s" data-recent-renewals-count="%s" data-upgrade-url="%s" data-keep-url="%s" data-compare-url="%s"',
        esc_attr($a['rules_url']), esc_attr($a['member_id']), esc_attr($a['current_tier']),
        esc_attr($a['credits_used_pct']), esc_attr($a['peak_bookings_14d']), esc_attr($a['waitlist_events_30d']),
        esc_attr($a['household_members']), esc_attr($a['has_annual']), esc_attr($a['recent_renewals_count']),
        esc_attr($a['upgrade_url']), esc_attr($a['keep_url']), esc_attr($a['compare_url'])
    );

    ob_start(); ?>
    <div class="nxs-upgrade-wrapper">
      <div class="nxs-upgrade" <?php echo $data_attrs; ?>></div>
      <noscript><em>This upgrade prompt requires JavaScript.</em></noscript>
    </div>
    <?php
    return ob_get_clean();
}
add_shortcode('nxs_upgrade_prompt', 'nxs_upgrade_prompt_shortcode');
